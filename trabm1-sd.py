import json
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# Pega o ID e a Sinopse do TMDB por meio do IMDB 
def get_tmdb_id(imdb_id):
    url = f"https://api.themoviedb.org/3/find/{imdb_id}?external_source=imdb_id"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyYzc4NTZjYjdmOTQ3YTYwYTk5OTc2ZmYxOGJmMzAyNyIsIm5iZiI6MTc0MzM0ODc4NS44NTEsInN1YiI6IjY3ZTk2NDMxYTk4ZGM4MTNiMGY2ZGVkZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.u8beRW8FeZtf-_dnvccwxpdF10y-7CGy2j7tqUF9Cy4"
    }

    response = requests.get(url, headers=headers).text

    data = json.loads(response)
    results = data.get("movie_results", [])
    if results:
        id = results[0].get("id")

        return id 
    
    return None


# Pega as reviews do respectivo filme
def get_tmdb_reviews(tmdb_id):
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/reviews?language=en-US&page=1"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyYzc4NTZjYjdmOTQ3YTYwYTk5OTc2ZmYxOGJmMzAyNyIsIm5iZiI6MTc0MzM0ODc4NS44NTEsInN1YiI6IjY3ZTk2NDMxYTk4ZGM4MTNiMGY2ZGVkZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.u8beRW8FeZtf-_dnvccwxpdF10y-7CGy2j7tqUF9Cy4"
    }

    response = requests.get(url, headers=headers).text

    data = json.loads(response)
    results = data.get("results", [])
    reviews_text = []
    for review in results[:3]:
        author_details = review.get("author_details", {})
        username = author_details.get("username", "Desconhecido")
        rating = author_details.get("rating")
        content = review.get("content", "")
    
        reviews_text.append({
            "username": username,
            "rating": rating,
            "content": content
        })


    return reviews_text

def get_plot(imdb_id, apikey):
    omdb_url = f"http://www.omdbapi.com/?apikey={apikey}&i={imdb_id}&plot=full"

    response = requests.get(url=omdb_url).text
    data = json.loads(response)
    plot = data.get("Plot", "Sinopse indisponível")

    return plot


# Formatação dos inputs
movie_name = input("Diga qual o nome do filme que deseja consultar: ").strip()
while movie_name == "":
    print("Você colocou um título vazio ou inválido, tente novamente")
    movie_name = input().strip()

movie_year = input("Qual seria o seu ano? ").strip()
while not movie_year.isdigit():
    print("Você colocou um ano vazio ou inválido, tente novamente")
    movie_year = input().strip()

movie_year = int(movie_year)


# Conexão com a omdb
omdb_apikey = "306f4c47"
omdb_url = f"http://www.omdbapi.com/?apikey={omdb_apikey}&s={movie_name}&y={movie_year}&type=movie&plot=full"

response = requests.get(url=omdb_url).text
data = json.loads(response)

if data.get('Response') == 'False':
    print(f"Erro: {data.get('Error')}")
    exit() 

movies = data.get("Search", [])

# Declaração da lista final
results_list = []

# Execução paralela
with ThreadPoolExecutor(max_workers=4) as executor:
    for movie in movies:
        imdb_id = movie.get("imdbID")
        title = movie.get("Title")
        year = movie.get("Year")

        future_plot = executor.submit(get_plot, imdb_id, omdb_apikey)
        future_tmdb_id = executor.submit(get_tmdb_id, imdb_id)
        
        plot = future_plot.result()
        tmdb_id = future_tmdb_id.result()
        
        if not tmdb_id:
            continue
        
        future_reviews = executor.submit(get_tmdb_reviews,tmdb_id)
        reviews = future_reviews.result()
        movie_result = {
            "titulo": title,
            "ano": int(year),
            "sinopse": plot,
            "reviews": reviews
        }

        results_list.append(movie_result)

final_json = json.dumps(results_list, indent=4, ensure_ascii=False)
print(final_json)