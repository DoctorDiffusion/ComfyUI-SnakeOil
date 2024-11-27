import os
import torch
import comfy.model_management
import comfy.utils
from comfy.sd import load_lora_for_models
from safetensors.torch import load_file

class SnakeOil:
    def __init__(self):
        self.loaded_lora = None

    @classmethod
    def INPUT_TYPES(cls):
        # Define the directory where LoRA models are stored using a relative path
        lora_directory = os.path.join(os.path.dirname(__file__), "..", "..", "models", "nloras")
        file_list = [f for f in os.listdir(lora_directory) if os.path.isfile(os.path.join(lora_directory, f))]
        file_list.insert(0, "None")
        return {
            "required": {
                "model": ("MODEL",),
                "nlora": (file_list, {"label": "nLoRA Model", "description": "Select the nLoRA model to apply"}),
                "snake_oil_amount": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 2.0, "step": 0.01, "display": "slider", "label": "Snake Oil Amount", "description": "Adjust the amount of Snake Oil to apply (0.0 to 2.0)"}),
            },
        }

    RETURN_TYPES = ("MODEL",)
    FUNCTION = "apply_snake_oil"
    CATEGORY = "🐍🛢️ Snake Oil"

    def apply_snake_oil(self, model, nlora, snake_oil_amount):
        if snake_oil_amount == 0:
            print("snake_oil_amount is 0, returning the original model.")
            return (model,)

        # Invert the snake_oil_amount value to its negative equivalent
        snake_oil_amount = -snake_oil_amount
        print(f"Inverted snake_oil_amount: {snake_oil_amount}")

        # Define the directory where LoRA models are stored using a relative path
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
            model_lora, _ = load_lora_for_models(model, None, lora, snake_oil_amount, 0)
            print(f"Successfully applied LoRA model with snake_oil_amount: {snake_oil_amount}")
        except Exception as e:
            print(f"Error applying LoRA model: {e}")
            return (model,)

        return (model_lora,)

# A dictionary that contains all nodes you want to export with their names
NODE_CLASS_MAPPINGS = {
    "SnakeOil": SnakeOil
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "SnakeOil": "🐍🛢️ Snake Oil"
}
