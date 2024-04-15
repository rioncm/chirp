import numpy as np
import tflite_runtime.interpreter as tflite

class Tensor:
    def __init__(self, model_path):
        # Load the TFLite model and allocate tensors
        self.interpreter = tflite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()

        # Get input and output details
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

    def preprocess(self, input_data):
        """Preprocess the input data to match the input tensor requirements."""
        # Ensure the input data type matches the model's input data type
        input_data = input_data.astype(self.input_details[0]['dtype'])
        # Resize the input as per the input tensor
        if input_data.shape != self.input_details[0]['shape']:
            input_data = np.resize(input_data, self.input_details[0]['shape'])
        return input_data

    def predict(self, input_data):
        """Run the model prediction on the input data."""
        # Process the input data
        input_data = self.preprocess(input_data)
        # Set the tensor to the correct input index
        self.interpreter.set_tensor(self.input_details[0]['index'], [input_data])
        # Run the interpreter
        self.interpreter.invoke()
        # Extract the output data from the output tensor
        output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
        return output_data

# Usage example
if __name__ == "__main__":
    model_path = 'path_to_your_model.tflite'  # Update this to your model's location
    tensor = Tensor(model_path)

    # Assuming `test_input` is your input data that matches the model's input shape and type
    test_input = np.random.random(tensor.input_details[0]['shape']).astype(tensor.input_details[0]['dtype'])
    result = tensor.predict(test_input)
    print("Model prediction:", result)
