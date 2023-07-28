import schoolmouv

# Videos
my_video = schoolmouv.video('https://www.schoolmouv.fr/cours/la-liberte-politique/cours-video')
my_video.run()
results = my_video.result # result found (list) (direct urls to mp4s)
my_video.download(results[0],'/path/to/folder',save_as='myvideo.mp4') # Default filename here is 'La liberte politique.mp4' (in this case)
my_video.see(results[0]) # Open in default browser

# PDFs
my_pdf = schoolmouv.pdf('https://www.schoolmouv.fr/cours/echantillonnage2/fiche-de-revision')
my_pdf.run()
result = my_pdf.result # result found (str) (direct url to pdf)
my_pdf.download(result,'/path/to/folder',save_as='mypdf.pdf') # Default filename is 'Echantillonage 2.pdf' (in this case)
my_pdf.see(result)