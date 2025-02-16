import import_ipynb
print("Importing notebook... It will show some commands, ignore them.")
import DSCI560_Lab5 as notebook
import sys
import time

def countdown(minutes):
    """Displays a countdown timer for the next update."""
    seconds = minutes * 60
    while seconds:
        mins, secs = divmod(seconds, 60)
        timer = f"Next update in {mins:02}:{secs:02} minutes..."
        print(timer, end="")
        time.sleep(1)
        seconds -= 1
    print("\n")  # Clear line




def main(interval):
    """Runs the full pipeline every `interval` minutes and allows user search in between."""
    subreddit_name = "askscience"
    n_posts = 5000  

    while True:
        print("Fetching and processing new Reddit posts...")
        notebook.fetch_and_store_reddit_posts(subreddit_name, n_posts)

        print("Generating embeddings and clustering messages...")
        
        posts = notebook.get_all_posts()
        print(len(posts))

        vectors_doc,model_doc = notebook.doc2Vec_embeddings(posts)
        print("Doc2Vec embeddings generated.")

        vectors_word,model_word = notebook.word2Vec_embeddings(posts)
        print("Word2Vec embeddings generated.")
        
        kmeans_doc,labeled_cluster_doc, cluster_doc = notebook.kmeans_clustering(vectors_doc, 5,posts)
        print("Doc2Vec clustering done.")

        kmeans_word,labeled_cluster_word,cluster_word = notebook.kmeans_clustering(vectors_word, 5,posts)
        print("Word2Vec clustering done.")
        
        notebook.store_cluster_labels(labeled_cluster_doc,labeled_cluster_word)
        print("Cluster labels stored in the database.")
        
        
        print(f"Data updated! Waiting {interval} minutes before next update...\n")
        

        
        while True:
            user_input = input("Enter a search query (or type 'skip' to continue automation): ")
            if user_input.lower() == "skip":
                break
            print(notebook.predict_similar_posts(user_input, model_doc, model_word, kmeans_doc, kmeans_word, posts))
            
        countdown(interval)



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: Please provide an interval in minutes. Example: `python automate.py 5`")
        sys.exit(1)

    interval = int(sys.argv[1])  
    main(interval)

