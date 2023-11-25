from db.crud import create_cheese
from db.session import get_db

cheeses = [
    {
        "name": "American Cheese",
        "description": "American Cheese is popular in the USA, great for sandwiches and burgers due to its creamy texture and good melting properties.",
        "image_path": "https://www.liveeatlearn.com/wp-content/uploads/2022/12/American-Cheese-650x395.jpg"
    },
    {
        "name": "Asiago Cheese",
        "description": "Asiago is an Italian cheese made from cow's milk, available either aged or immature, with a stronger flavor when aged.",
        "image_path": "https://www.liveeatlearn.com/wp-content/uploads/2022/12/Asiago-Cheese-650x434.jpg"
    },
    {
        "name": "Blue Cheese",
        "description": "Blue Cheese, known for its blue spots and veins, offers a spicy taste and is used in various dishes like blue cheese dressing.",
        "image_path": "https://www.liveeatlearn.com/wp-content/uploads/2022/12/Blue-Cheese-650x394.jpg"
    },
    {
        "name": "Brocconcini",
        "description": "Brocconcini are small mozzarella balls with a soft, spongy texture, often eaten whole or in salads.",
        "image_path": "https://www.liveeatlearn.com/wp-content/uploads/2022/12/Brocconcini.jpg"
    },
    {
        "name": "Brie Cheese",
        "description": "Brie, a soft and silky cheese, comes in a round wheel with a light crust, often eaten with crackers or bread.",
        "image_path": "https://www.liveeatlearn.com/wp-content/uploads/2022/12/Brie-Cheese-650x363.jpg"
    },
    {
        "name": "Burrata Cheese",
        "description": "Burrata, a semi-soft white cheese made with buffalo milk, resembles mozzarella but with a soft milky interior, great on salads and pizzas.",
        "image_path": "https://www.liveeatlearn.com/wp-content/uploads/2022/12/Burrata-Cheese-650x423.jpg"
    },
    {
        "name": "Butterkäse",
        "description": "Butterkase, a semi-soft, mildly salty cheese with a smooth, creamy texture, is versatile for sandwiches and cooking.",
        "image_path": "https://www.liveeatlearn.com/wp-content/uploads/2022/12/Butterka%CC%88se-650x432.jpg"
    },
    {
        "name": "Cabrales",
        "description": "Cabrales, a Spanish variant of blue cheese, is made exclusively in the Asturias region with specific milk types, offering a unique flavor.",
        "image_path": "https://www.liveeatlearn.com/wp-content/uploads/2022/12/Cabrales.jpg"
    },
    {
        "name": "Camembert Cheese",
        "description": "Camembert, similar to brie but with a more intense flavor, is not as spreadable, often enjoyed with crackers and jam.",
        "image_path": "https://www.liveeatlearn.com/wp-content/uploads/2022/12/Camembert-Cheese-650x367.jpg"
    },
    {
        "name": "Cheddar Cheese",
        "description": "Cheddar, America’s top selling cheese, ranges from mild to sharp and creamy, perfect for melting on burgers and in various dishes.",
        "image_path": "https://www.liveeatlearn.com/wp-content/uploads/2022/12/Cheddar-Cheese-650x343.jpg"
    }
]


db = next(get_db())

for cheese in cheeses:
    create_cheese(db, **cheese)
