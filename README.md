<h1>Twitter Community Notes Health Analysis<h/1>
<h3>Where to download the community note data</h3>
  
https://communitynotes.x.com/guide/en/under-the-hood/download-data

<h3>How to clean the data</h3>
<ul>
  <li>On the site listed above, click on the download data link, and log into Twitter</li>
  <li>Download the top file, rename it to "rawCommunityNotes.tsv", place it into the project,</li> 
<h3>Run HealthFilter.py and then EnglishFilter.py</h3>

  <li>Under the first download link, download only the first ratings link, rename it to "ratings.tsv", place it in your project,</li>
<h3>run RatingsMerge.py</h3>

  <li>You should be left with "communityNotesFinalNoRatings.tsv" and "communityNotesFinalWithRatings.tsv"</li>
  <li>All other .tsv files should be deleted</li>

  <h3>Then do "python HelpfulResults.py" to run the application.</h3>
<li>Once ran ask health related questions and then will reponse with similar community notes using NLP and ML</li>
</ul>
<h1>About Health Application</h1>
<li>The app starts of loading and filtering all the X Community Notes into Health Related Terms. 

It Then prompts the user to ask a health related question, then once the user clicks search it displays the top 3 results according to similarities and matching terms.

The results also provide the note ID, Similarity Score, Helpfulness, Matching Terms, and the Date the note was written. 

This data was gathered through our other python scripts we created to gather information.</li>
