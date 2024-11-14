import requests
import openai
import easygui

# text link
address = "https://cdn.oxido.pl/hr/Zadanie%20dla%20JJunior%20AI%20Developera%20-%20tresc%20artykulu.txt"
# I assumed that we have to get the text from web.
# Just in case I will write code to access it locally (downloaded before)
just_in_case = "artykul.txt"

# article file name
file = "artykul.html"

# prompt to generate article
prompt = 'Przedstaw treść z sugestiami miejsc na grafiki w formacie HTML, ale jedynie treść do wstawienia pomiędzy tagami <body> i </body>, bez nagłówka HTML. Wstaw znaczniki <img src="image_placeholder.jpg" alt="prompt do generacji grafiki"> w odpowiednich miejscach. Atrybut alt powinien zawierać dokładny prompt do wygenerowania obrazu pasującego do kontekstu, a pod każdym obrazem dodaj opis obrazka, używając znacznika <figcaption>.'


def get_code():
    code = easygui.enterbox("Enter OpenAI code:")
    return code


openai.api_key = get_code()


# func to get text from web
def getting_text_from_web(link):
    try:
        txt = requests.get(link, timeout=2)
        txt.raise_for_status()
        txt = txt.text
        return txt.encode('iso-8859-1').decode('utf-8')
    except requests.exceptions.Timeout:
        print("Couldn't reach the link")
        return None
    except requests.exceptions.RequestException as error:
        print(f"{error} error")
        return None


# func to get text locally
def getting_text_locally(f):
    with open(f, 'r') as c:
        txt = c.read()
        return txt.encode('iso-8859-1').decode('utf-8')


# func to get text either from web or locally
def source_text_validation(a, f):
    t = getting_text_from_web(a)
    if t:
        return t
    else:
        t = getting_text_locally(f)
        return t


def saving_article(f, t):
    with open(f, "w") as article:
        article.write(t)


def generating_article(prom, input_text):
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # or "gpt-4.0-turbo" based on your needs
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"{prom}\n\n{input_text}"}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        # Make the API call to OpenAI with the provided prompt and input text

        # Extract the generated text from the response
        generated_text = response.choices[0].message.content

        return generated_text

    except Exception as e:
        print("An error occurred:", e)
        return None


def main():
    # getting text
    text = source_text_validation(address, just_in_case)
    # generating article
    article = generating_article(prompt, text)
    if article:  # saving if all is ok
        saving_article(file, article)
        print("Done")
    else:
        print("Couldn't generate article :(")


if __name__ == '__main__':
    main()
