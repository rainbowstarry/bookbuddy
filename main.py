import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

while True:
    choice = input("do you want to continue, type yes to continue, no to exit")
    if choice == "no":
        break
    else:
        number = int(input("do you want to get a book recommendation (0), or potentially find a BookBuddy? (1)"))
        if number == 1:
            pp = pd.read_csv('books.csv', encoding='unicode_escape')

            firstname = input("enter your first name: ")
            secondname = input("enter your second name: ")
            email = input("enter your email: ")
            title = input("enter your favourite book's title: ")
            genre = input(
                "enter your favourite genre (either Fiction, Dystopian, Classic Literature, Fantasy, Magical Realism, Mystery or Young Adult): ")
            author = input("enter your favourite author: ")
            uni = input("enter your university: ")
            id = pp.shape[0]
            pp.loc[len(pp.index)] = [id, firstname, secondname, email, title, genre, author, uni]
            # create a list of columns which are used to decide
            columns = ['title', 'genre', 'author', 'university']


            # create a function to combine the important columns/features
            def combine_column(data):
                feature = []
                for i in range(0, data.shape[0]):
                    feature.append(
                        data['title'][i] + ' ' + data['genre'][i] + ' ' + data['author'][i] + ' ' + data['university'][
                            i])
                return feature


            pp['combined_feature'] = combine_column(pp)
            # convert the text from the new column to a matrix of word counts
            cm = CountVectorizer().fit_transform(pp['combined_feature'])
            # get the cosine similarity matrix from the count matrix
            cs = cosine_similarity(cm)

            # #create a list of tuples in the form (book_id, similarity score)
            scores = list(enumerate(cs[id]))
            # #sort the list of similar books in descending order
            sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
            sorted_scores = sorted_scores[1:]
            # #create a loop to print the first 5 books from the sorted list
            j = 0
            print('The 5 most recommended people and their emails are:\n')
            for item in sorted_scores:
                name = (pp[pp.pid == item[0]]['firstname'].values[0]) + ' ' + (
                    pp[pp.pid == item[0]]['secondname'].values[0])
                mailaddress = pp[pp.pid == item[0]]['email'].values[0]
                print(j + 1, name, mailaddress)
                j = j + 1
                if j >= 5:
                    break
            while True:
                choice = input("if you want to see someone's profile, enter their first name, if not, type no")
                if choice == "no":
                    break
                else:
                    id = pp[pp.firstname == choice]['pid'].values[0]
                    print('favourite book: ', pp.loc[id, 'title'])
                    print('favourite genre: ', pp.loc[id, 'genre'])
                    print('favourite author: ', pp.loc[id, 'author'])
                    print('university: ', pp.loc[id, 'university'])
        elif number == 0:

            df = pd.read_csv('book.csv', encoding='unicode_escape')
            # create a list of columns to keep
            columns = ['title', 'authors', 'language_code']


            # create a function to combine the important columns/features
            def combine_features(data):
                features = []
                for i in range(0, data.shape[0]):
                    features.append(data['title'][i] + ' ' + data['authors'][i] + ' ' + data['language_code'][i])
                return features


            df['combined_features'] = combine_features(df)
            # convert the text from the new column to a matrix of word counts
            cm = CountVectorizer().fit_transform(df['combined_features'])
            # get the cosine similarity matrix from the count matrix
            cs = cosine_similarity(cm)
            # get the title of the book the reader likes
            Title = input("enter the title of the book you like")
            # find the book id of the book that the user likes
            book_id = df[df.title == Title]['bookID'].values[0]
            # create a list of tuples in the form (book_id, similarity score)
            scores = list(enumerate(cs[book_id]))
            # sort the list of similar books in descending order
            sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
            sorted_scores = sorted_scores[1:]
            # create a loop to print the first 5 books from the sorted list
            j = 0
            print('The 5 most recommended books to ' + Title + ' are:\n')
            for item in sorted_scores:
                book_title = df[df.bookID == item[0]]['title'].values[0]
                print(j + 1, book_title)
                j = j + 1
                if j >= 5:
                    break
