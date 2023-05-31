import wikipedia
wikipedia.set_lang('ru')
result = wikipedia.search("Москва")
page = wikipedia.page(result[0])
categories = page.categories
print(categories)
content = page.summary