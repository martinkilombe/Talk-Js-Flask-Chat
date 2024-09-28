1. Set up the Python environment:
   ```
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Create a `.env` file in the project root and add your TalkJS App ID:
   ```
   TALKJS_APP_ID=your_talkjs_app_id_here
   ```

3. Run the Flask application:
   ```
   python app.py
   ```

4. Open a web browser and navigate to `http://localhost:8080`

Note: Ensure your virtual environment is activated (step 1) whenever you're working on the project.