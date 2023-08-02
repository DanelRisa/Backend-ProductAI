import openai
import os


class ChatGPTService:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = api_key
    
    def get_products_by_dish(self, dish_name:str) -> list[str]:
        prompt = f'хочу приготовить: {dish_name}'
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "напиши список продуктов для приготовления блюда " + prompt + " и укажи категорию для каждого продукта исходя из его названия и предназначения. Напиши название продукта, затем черточку (-), затем категорию из следующих: Бакалея, Овощи и фрукты, Колбасы и сыры, Кондитерские изделия, Консервы, Молочные продукты и яйца, Напитки и алкогольные напитки, Полуфабрикаты, Хлеб и хлебобулочные изделия, Чай и кофе и какао, Мясо и рыба и птица. Если зелень, мясо, специи, то укажи соответствующую категорию. НЕ ИСПОЛЬЗУЙ СКОБКИ. Convert answer to JSON format."}
            ],
        max_tokens=9000,
        n=1,
        stop=None,
        temperature=0.0,
        api_key=self.api_key
        )
        
        return completion.choices[0].message.get("content", "")
    
    def get_product_by_category(self, product_name:str) ->str:
        prompt = f'{product_name}'
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "определи в какой из перечисленных категорий относится " + prompt + " исходя из названия продукта и его предназначени: Бакалея, Овощи и фрукты, Колбасы и сыры, Кондитерские изделия, Консервы, Молочные продукты и яйца, Напитки и алкогольные напитки, Полуфабрикаты, Хлеб и хлебобулочные изделия, Чай и кофе и какао, Мясо и рыба и птица. Напиши ответ в виде название продукта, категории и  ничего лишнего. Если зелень, мясо, специи то сразу уточни какая, не используй слово зелень. Если растительное масло то напиши сразу какой подсолнечное масло или другие виды. Пиши название продукта - категорию. Convert answer to JSON format"},
            ],
            max_tokens=9000,
            n=1,
            stop=None,
            temperature=0.0,
            api_key=self.api_key
        )

        return completion.choices[0].message.get("content", "")
 
