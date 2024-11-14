import requests
import openai
import os

key = ""

openai.api_key = key


# text link
address = "https://cdn.oxido.pl/hr/Zadanie%20dla%20JJunior%20AI%20Developera%20-%20tresc%20artykulu.txt"

# I assumed that we have to get the text from web.
# Just in case I will write code to access it locally (downloaded before)
just_in_case = "artykul.txt"
# article address
file = "artykul.html"

prompt = 'Przedstaw treść z sugestiami miejsc na grafiki w formacie HTML, ale jedynie treść do wstawienia pomiędzy tagami <body> i </body> . Wstaw znaczniki <img src="image_placeholder.jpg" alt="prompt do generacji grafiki"> w odpowiednich miejscach. Atrybut alt powinien zawierać dokładny prompt do wygenerowania obrazu pasującego do kontekstu, a pod każdym obrazem dodaj opis obrazka, używając znacznika <figcaption>.'


# func to get text
def getting_text(link):
    # just in case
    """with open(just_in_case, 'r') as c:
        txt = c.read()
        return txt.encode('iso-8859-1').decode('utf-8')
    """
    try:
        txt = requests.get(link, timeout=2)
        txt.raise_for_status()
        txt = txt.text
        return txt.encode('iso-8859-1').decode('utf-8')
    except requests.exceptions.Timeout:
        print("Couldn't reach the link")
    except requests.exceptions.RequestException as error:
        print(f"{error} error")


def saving_article(f, t):
    with open(f, "w") as article:
        article.write(t)


def generating_article(prom, input_text):
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # or "gpt-3.5-turbo" based on your needs
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

        try:
            with open("test2.html", "w", encoding="utf-8") as t2:
                t2.write(generated_text)
            print("HTML content saved successfully.")
        except Exception as e:
            print("An t2 error occurred:", e)

        return generated_text

    except Exception as e:
        print("An t2 error occurred:", e)
        return None


def main():
    # getting text
    text = getting_text(address)
    article = generating_article(prompt, text)
    if article:
        saving_article(file, article)
        print("Done")
    else:
        print("Couldn't generate article :(")


main()
