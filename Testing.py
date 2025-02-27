import datetime
def Generate_Article_Design(Author, Content, Date, Name):
    print(f"\n{'='*40}")
    print(f"Title: {Name}")
    print(f"By: {Author} on {Date}")
    print(f"{'-'*40}\n{Content}\n{'='*40}\n")


Generate_Article_Design("Boudi", "I love to program and play chess, I love myself and who i am", datetime.datetime.now().date(), "About myself")