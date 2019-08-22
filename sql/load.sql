CREATE TABLE artist (
	artist_id INTEGER PRIMARY KEY,
	artist_name VARCHAR(255)
);


CREATE TABLE token (
	song_id INTEGER,
	token VARCHAR(255),
	count INTEGER,
	PRIMARY KEY (song_id, token)
);

CREATE TABLE song (
	song_id INTEGER PRIMARY KEY,
	artist_id INTEGER REFERENCES artist(artist_id),
	song_name VARCHAR(255),
	page_link VARCHAR(1000)
	/* , FOREIGN KEY (artist_id) REFERENCES artist (artist_id) */
);

CREATE TABLE tfidf (
	song_id INTEGER,
	token VARCHAR(255),
	score FLOAT,
	PRIMARY KEY(song_id, token)
);


COPY artist FROM '/home/cavan/OldClasses/cs143/TuneSearch/data/artist.csv' DELIMITER ',' QUOTE '"' CSV;
COPY song   FROM '/home/cavan/OldClasses/cs143/TuneSearch/data/song.csv'   DELIMITER ',' QUOTE '"' CSV;
COPY token  FROM '/home/cavan/OldClasses/cs143/TuneSearch/data/token.csv'  DELIMITER ',' QUOTE '"' CSV;

INSERT INTO tfidf 
SELECT a.song_id, a.token, a.count*log((SELECT COUNT(*) FROM song)/b.song_num) as tfidf 
FROM token as a, (SELECT COUNT(song_id) as song_num, token FROM token GROUP BY token) as b 
WHERE a.token = b.token;

