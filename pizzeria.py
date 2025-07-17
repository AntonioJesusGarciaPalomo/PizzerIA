import asyncio
import os
from dotenv import load_dotenv

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.azure_chat_prompt_execution_settings import (
    AzureChatPromptExecutionSettings,
)
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.functions import kernel_function
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior

load_dotenv()

endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
api_key = os.environ.get("AZURE_OPENAI_API_KEY")
deployment_name = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME") 
api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-01")


chat_service = AzureChatCompletion(
    deployment_name=deployment_name,
    api_key=api_key,
    endpoint=endpoint,
    api_version=api_version,
)

class PizzaMenuPlugin:
    @kernel_function(name="get_available_pizzas", description="Retrieves the list of available pizzas with their details")
    async def get_available_pizzas(self):
        return [
            {"name": "Pepperoni", "ingredients": "Pepperoni, cheese, tomato sauce", "price": 12},
            {"name": "Margherita", "ingredients": "Tomato, mozzarella, basil", "price": 10},
            {"name": "Hawaiian", "ingredients": "Ham, pineapple, cheese", "price": 11},
            {"name": "Vegetarian", "ingredients": "Mushrooms, peppers, onions, olives", "price": 13}
        ]


class CartService:
    cart_items = []
    
    @classmethod
    def add_item(cls, item):
        cls.cart_items.append(item)
    
    @classmethod
    def remove_item(cls, item):
        if item in cls.cart_items:
            cls.cart_items.remove(item)
            return True
        return False
    
    @classmethod
    def clear_cart(cls):
        cls.cart_items.clear()


class ShoppingCartPlugin:
    @kernel_function(name="add_to_cart", description="Adds a pizza to the shopping cart")
    async def add_to_cart(self, pizza_name: str):
        CartService.add_item(pizza_name)
        return f"{pizza_name} added to cart."
    
    @kernel_function(name="remove_from_cart", description="Removes a pizza from the shopping cart")
    async def remove_from_cart(self, pizza_name: str):
        removed = CartService.remove_item(pizza_name)
        return f"{pizza_name} removed from cart." if removed else "Item not found in cart."
    
    @kernel_function(name="view_cart", description="Displays the current contents of the shopping cart")
    async def view_cart(self):
        return CartService.cart_items.copy()
    
    @kernel_function(name="clear_cart", description="Clears all items from the shopping cart")
    async def clear_cart(self):
        CartService.clear_cart()
        return "Cart cleared."

class PaymentPlugin:
    @kernel_function(name="process_payment", description="Processes the payment for the current order. Calculates total automatically.")
    async def process_payment(self, payment_method: str):
        valid_methods = ["tarjeta", "efectivo"]
        if payment_method.lower() not in valid_methods:
            return f"Error: Payment method '{payment_method}' is not supported."
        
        total = self._calculate_total()
        if total == 0:
            return "Error: Cart is empty."
        
        CartService.clear_cart()
        return f"Payment of ${total:.2f} via {payment_method} processed successfully!"
    
    def _calculate_total(self):
        prices = {"Pepperoni": 12.0, "Margherita": 10.0, "Hawaiian": 11.0, "Vegetarian": 13.0}
        return sum(prices.get(item, 0.0) for item in CartService.cart_items)

kernel = Kernel()
kernel.add_plugin(PizzaMenuPlugin(), plugin_name="PizzaMenuPlugin")
kernel.add_plugin(ShoppingCartPlugin(), plugin_name="ShoppingCartPlugin")
kernel.add_plugin(PaymentPlugin(), plugin_name="PaymentPlugin")
kernel.add_service(chat_service)

async def main():
    
    history = ChatHistory()
    
    while True:
                    
        user_input = input("\n🧑 User > ")

        if user_input.lower() in ["exit", "quit", "salir"]:
            print("👋 ¡Hasta luego!")
            break
        
        if not user_input.strip():
            print("Por favor, escribe un mensaje.")
            continue
        
        history.add_user_message(user_input)
                    
        settings = AzureChatPromptExecutionSettings(
            function_choice_behavior=FunctionChoiceBehavior.Auto(),
            max_tokens=1000,
            temperature=0.7
        )
                    
        response = await chat_service.get_chat_message_content(
            chat_history=history,
            settings=settings,
            kernel=kernel,
        )
        
        print(f"🤖 AI > {response}")
        await asyncio.sleep(0.1)              
        history.add_message(response)

    

if __name__ == "__main__":

    if os.name == "nt":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())