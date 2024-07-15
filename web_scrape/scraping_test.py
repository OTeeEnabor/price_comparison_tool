import helpers

from pathlib import Path
path = str(Path.cwd())
print(path,type(path))
# product_list = [
#     "Corona Extra Beer Bottles 24 x 355ml",
#     "Bernini Classic Sparkling Grape Frizzante Bottles 6 x 275ml",
#     "Coca-Cola No Sugar Soft Drink 4 x 6 x 300ml",
#     "Jacobs Gold Freeze Dried Instant Coffee 47.5g",
#     "NESCAFÉ Gold Instant Hazelnut Cappuccino Sticks 20 x 18g",
#     "Cappy Still Orange Mango Fruit Juice Blend Bottle 1.5L",
#     "Tante Anna Crushed Wholewheat Brown Bread 700 g",
#     "Our Ultimate Burger Buns 4 x 80 g",
#     "Fresh Custard with Vanilla Bean Seeds 500 ml",
#     "Chocolate & White Chocolate Mousse Swirls 3 x 125 ml",
#     "Amagwinya Vetkoek 4 pk",
#     "Product name White Bread Dough 1kg",
# ]

# for product in product_list:
#     weight_components_list = helpers.get_weight_components(product)
#     weight_unit = None
#     if weight_components_list != None:
#         weight_unit = helpers.get_weight_unit(weight_components_list[-1])

#     print(
#         f"name: {product} - weight components:{weight_components_list} - unit: {weight_unit} - product-weight: {helpers.get_product_weight(product)}"
#     )
