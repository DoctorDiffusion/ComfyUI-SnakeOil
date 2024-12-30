import os
import torch
import comfy.model_management
import comfy.utils
from comfy.sd import load_lora_for_models
from safetensors.torch import load_file

class NegativeLoRALoader:
    def __init__(self):
        self.loaded_lora = None

    @classmethod
    def INPUT_TYPES(cls):
        # Define the directory where nLoRA models are stored using a relative path
        lora_directory = os.path.join(os.path.dirname(__file__), "..", "..", "models", "nloras")

        def list_safetensors_files(directory):
            file_list = []
            for root, _, files in os.walk(directory):
                for file in files:
                    if file.endswith(".safetensors"):
                        file_list.append(os.path.relpath(os.path.join(root, file), directory))
            return file_list

        file_list = list_safetensors_files(lora_directory)
        file_list.insert(0, "None")
        return {
            "required": {
                "model": ("MODEL",),
                "nlora": (file_list, {"label": "nLoRA Model", "description": "Select the nLoRA model to apply"}),
                "inverted_strength_value": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 2.0, "step": 0.01, "display": "slider", "label": "Snake Oil Amount", "description": "Adjust the amount of Snake Oil to apply (0.0 to 2.0)"}),
            },
        }

    RETURN_TYPES = ("MODEL",)
    FUNCTION = "apply_inverted_LoRA"
    CATEGORY = "🐍🛢️ Snake Oil"

    def apply_snake_oil(self, model, nlora, inverted_strength_value):
        if inverted_strength_value == 0:
            print("inverted_strength_value is 0, returning the original model.")
            return (model,)

        # Invert the inverted_strength_value value to its negative equivalent haha yes really
        inverted_strength_value = -inverted_strength_value
        print(f"Inverted inverted_strength_value: {inverted_strength_value}")

        # Define the directory where nLoRA models are stored using a relative path again maybe
        lora_directory = os.path.join(os.path.dirname(__file__), "..", "..", "models", "nloras")
        lora_path = os.path.join(lora_directory, nlora)

        print(f"Loading LoRA from: {lora_path}")

        lora = None
        if self.loaded_lora is not None:
            if self.loaded_lora[0] == lora_path:
                lora = self.loaded_lora[1]
            else:
                temp = self.loaded_lora
                self.loaded_lora = None
                del temp

        if lora is None:
            try:
                lora = load_file(lora_path)
                self.loaded_lora = (lora_path, lora)
                print(f"Successfully loaded LoRA model from: {lora_path}")
            except Exception as e:
                print(f"Error loading LoRA model: {e}")
                return (model,)

        try:
            model_lora, _ = load_lora_for_models(model, None, lora, inverted_strength_value, 0)
            print(f"Successfully applied LoRA model with inverted_strength_value: {inverted_strength_value}")
        except Exception as e:
            print(f"Error applying LoRA model: {e}")
            return (model,)

        return (model_lora,)

# A dictionary that contains all nodes you want to export with their names
NODE_CLASS_MAPPINGS = {
    "NegativeLoRALoader": NegativeLoRALoader
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "NegativeLoRALoader": "Negative LoRA Loader"
}
