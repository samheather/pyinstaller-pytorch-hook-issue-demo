import setuptools
from imaginairy import imagine, imagine_image_files, ImaginePrompt, WeightedPrompt, LazyLoadingImage

prompts = [
    ImaginePrompt("a bowl of fruit")
]
for result in imagine(prompts):
    result.save("my_image.jpg")