import torch
from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor, BitsAndBytesConfig
from pdf2image import convert_from_path
from PIL import Image


class OCRModel:
    def __init__(self, model_name):
        self.model_name = model_name
        self.model, self.processor = self.initialize_model()

    def initialize_model(self):
        quantization_config = BitsAndBytesConfig(
            load_in_8bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
            llm_int8_enable_fp32_cpu_offload=True,
        )
        model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
            self.model_name, device_map="auto", quantization_config=quantization_config
        )
        processor = AutoProcessor.from_pretrained(self.model_name)
        return model, processor

    def process_pdf(self, pdf_path):
        images = convert_from_path(pdf_path)
        return images

    def process_text(self, text):
        pass
        
    def extract_details(self, image):
        messages = [
            {"role": "system", "content": "Extract merchant name, total amount, and purchase date from this receipt."}
        ]
        text = self.processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = self.processor(
            text=[text],
            images=[image],
            padding=True,
            return_tensors="pt",
        )

        with torch.no_grad():
            generated_ids = self.model.generate(
                **inputs,
                max_new_tokens=128,
                do_sample=False,
                temperature=0.7,
                top_k=50,
                top_p=0.9,
            )
        generated_ids_trimmed = [
            out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
        ]
        results = self.processor.batch_decode(
            generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
        )

        result = results[0] if results else None
        

        return results[0] if results else None

    def process_images(self, pdf_path):
        images = self.process_pdf(pdf_path)
        extracted_data = []
        
        for i, image in enumerate(images):
            result = self.extract_details(image)
            if result and ("merchant" in result.lower() or "amount" in result.lower() or "date" in result.lower()):
                extracted_data.append(result)
        
        return extracted_data