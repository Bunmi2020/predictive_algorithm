1. **Install python**

2. **Create a Virtual Environment (Optional but Recommended)**
   
   ```powershell
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```
   
3. **Install Dependencies**
   
   ```bash
   pip install numpy
   ```
   
4. **test fixtures**
   eredivisie.json in the root folder is the test fixtures. the python has been written to incorporate the data and export the predictions per each of the fixture.

   run the pred_one.python to see

5. **other additional conditions**
    


For corners: Check defensive style for "" Check attacking style for "wide play" and "High Line; Use offside positioning" they tend to have more corners, and "deep"

For cards: check defensive style for "Non-aggressive": they concede less fouls and receive less cards. or 'aggressive'. check attacking style for "Opponents play aggressively against them" they win more fouls. Also count the number of aggressive and provocative players combine for each feature; the higher the number the more cards.

For 1x:2x:no draw, add an array of form and another object indicating league position for each team in team'
Also for corners 1_2, create form array

If h2h W or D for team1 => 2 and recent_games > 3 ...team1 
Elif
If if h2h W or D for team1 => 2 and recent_games > 3 ...team1 
Elif 
h2h D for team1 <= 2 and in recent_games < 3 ...no draw
Else
Can not predict, too many inconsistencies

for cards, the condition for Ov 3.5, add if aggressive and provocative players for home and away > 2 each, and there is aggressive in playing style: then prediction is: O 4.5

These are current conditions; if you can help incorporate them in the current algorithm, then I can help develop it further. Let me know.