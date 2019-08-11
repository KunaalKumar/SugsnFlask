import re


class MovieItem:
    def __init__(self, listNum, imdbId, name, year, filmRating, runTime, genre, imdbRating, metaScore, description, posterUrl):
        self.listNum = int(re.sub("[^0-9]", "", listNum), 10)
        self.imdbId = imdbId
        self.name = name
        self.year = int(re.search("[0-9]{4}", year).group(0), 10)
        self.filmRating = filmRating
        self.runTime = runTime
        self.genre = genre.strip()
        self.imdbRating = float(imdbRating)
        self.metaScore = int(metaScore.strip())
        self.description = description.strip()
        # Replace to increase poster resolution
        self.posterUrl = posterUrl.replace(".jpg", "#\$1.jpg")

        # Generate rotten rating
        self.rottenRating = getRottenMovieRating(self.name, self.year)

    def __str__(self):
        return self.listNum
