# Jarjit

<picture>
	<img src="assets/icon.png" align="right" alt="Jarjit Logo" width="120" height="120">
</picture>

### Full Autopilot for All Computers Using LLMs

Jarjit
- Self-drives computers by sending user requests to an LLM backend (GPT-4V, etc) to figure out the required steps.
- Automatically executes the steps by simulating keyboard and mouse input.
- Course-corrects by sending the LLMs a current screenshot of the computer as needed. 


<div align="center">
<h4>Self-Driving Software for All Your Computers</h4>

  [![macOS](https://img.shields.io/badge/mac%20os-000000?style=for-the-badge&logo=apple&logoColor=white)](https://github.com/zaikaman/Jarjit?tab=readme-ov-file#install)
  [![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)](https://github.com/zaikaman/Jarjit?tab=readme-ov-file#install)
  [![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)](https://github.com/zaikaman/Jarjit?tab=readme-ov-file#install)
  <br>
  [![Github All Releases](https://img.shields.io/github/downloads/zaikaman/Jarjit/total.svg)]((https://github.com/zaikaman/Jarjit/releases/latest))
  ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/zaikaman/Jarjit)
  ![GitHub Repo stars](https://img.shields.io/github/stars/zaikaman/Jarjit)
  ![GitHub](https://img.shields.io/github/license/zaikaman/Jarjit) 
  [![GitHub Latest Release)](https://img.shields.io/github/v/release/zaikaman/Jarjit)](https://github.com/zaikaman/Jarjit/releases/latest)

</div>

### <ins>Demo</ins> 💻
["Make me a meal plan in Google Docs"]<br>
![Make Meal Plan Demo](assets/meal_plan_demo_2x.gif)<br>
[More Demos](https://github.com/zaikaman/Jarjit/blob/main/MEDIA.md#demos)



<hr>

### <ins>Install</ins> 💽
<details>
    <summary><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Apple_Computer_Logo_rainbow.svg/640px-Apple_Computer_Logo_rainbow.svg.png" alt="MacOS Logo" width="13" height="15"> <b>MacOS</b></summary>
    <ul>
        <li>Download the MacOS binary from the latest <a href="https://github.com/zaikaman/Jarjit/releases/latest">release</a>.</li>
        <li>Unzip the file and move Jarjit to the Applications Folder.<br><br> 
            <img src="assets/macos_unzip_move_to_applications.png" width="350" style="border-radius: 10px;
    border: 3px solid black;">
        </li>
    </ul>
  <details>
    <summary><b>Apple Silicon M-Series Macs</b></summary>
    <ul>
      <li>
        jarjit will ask you for Accessibility access to operate your keyboard and mouse for you, and Screen Recording access to take screenshots to assess its progress.<br>
      </li>
      <li>
        In case it doesn't, manually add these permission via <b>System Settings</b> -> <b>Privacy and Security</b>
        <br>
        <img src="assets/mac_m3_accessibility.png" width="400" style="margin: 5px; border-radius: 10px;
    border: 3px solid black;"><br>
        <img src="assets/mac_m3_screenrecording.png" width="400" style="margin: 5px; border-radius: 10px;
    border: 3px solid black;">
      </li>
    </ul>
  </details>
  <details>
    <summary><b>Intel Macs</b></summary>
    <ul>
        <li>
            Launch the app from the Applications folder.<br>
            You might face the standard Mac <i>"Jarjit cannot be opened" error</i>.<br><br>
            <img src="assets/macos_unverified_developer.png" width="200" style="border-radius: 10px;
    border: 3px solid black;"><br>
            In that case, press <b><i><ins>"Cancel"</ins></i></b>.<br>
            Then go to <b>System Preferences -> Security and Privacy -> Open Anyway.</b><br><br>
            <img src="assets/macos_system_preferences.png" width="100" style="border-radius: 10px;
    border: 3px solid black;"> &nbsp; 
            <img src="assets/macos_security.png" width="100" style="border-radius: 10px;
    border: 3px solid black;"> &nbsp;
            <img src="assets/macos_open_anyway.png" width="400" style="border-radius: 10px;
    border: 3px solid black;"> 
        </li>
        <br>
        <li>
        Jarjit will also need Accessibility access to operate your keyboard and mouse for you, and Screen Recording access to take screenshots to assess its progress.<br><br>
        <img src="assets/macos_accessibility.png" width="400" style="margin: 5px; border-radius: 10px;
    border: 3px solid black;"><br>
        <img src="assets/macos_screen_recording.png" width="400" style="margin: 5px; border-radius: 10px;
    border: 3px solid black;">
        </li>
      </ul>
</details>
      <ul>
        <li>Lastly, checkout the <a href="#setup">Setup</a> section to connect jarjit to LLMs (OpenAI GPT-4V)</li>
    </ul>
</details>
<details>
    <summary><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/TuxFlat.svg/640px-TuxFlat.svg.png" alt="Linux Logo" width="15" height="15"> <b>Linux</b></summary>
    <ul>
        <li>Linux binary has been tested on Ubuntu 20.04 so far.</li>
        <li>Download the Linux zip file from the latest <a href="https://github.com/zaikaman/Jarjit/releases/latest">release</a>.</li>
        <li>
            Extract the executable and run it from the Terminal via <br>
            <code>./Jarjit</code>
        </li>
	<li>Checkout the <a href="https://github.com/zaikaman/Jarjit?tab=readme-ov-file#setup">Setup</a> section to connect Jarjit to LLMs (OpenAI GPT-4V)</li>
    </ul>
</details>
<details>
    <summary><img src="https://upload.wikimedia.org/wikipedia/commons/5/5f/Windows_logo_-_2012.svg" alt="Linux Logo" width="15" height="15"> <b>Windows</b></summary>
    <ul>
	<li>Windows binary has been tested on Windows 10.</li>
	<li>Download the Windows zip file from the latest <a href="https://github.com/zaikaman/Jarjit/releases/latest">release</a>.</li>
	<li>Unzip the folder, move the exe to the desired location, double click to open, and voila.</li>
	<li>Checkout the <a href="https://github.com/zaikaman/Jarjit?tab=readme-ov-file#setup">Setup</a> section to connect Jarjit to LLMs (OpenAI GPT-4V)</li>
    </ul>
</details>


### <ins id="setup">Setup</ins> 🛠️
<details>
    <summary><b>Set up the GitHub API key</b></summary>

- Get your GitHub API key
  - Jarjit needs access to GitHub's API to perform user requests. 
  - Go to your [GitHub Settings](https://github.com/settings/tokens) and generate a new Personal Access Token
  - Select the "Generate new token (classic)" option
  - Give it a name (e.g., "Jarjit Access Token")
  - For scopes, you only need `read:user` and `user:email`
  - Copy the generated token immediately as you won't be able to see it again

- Save the API key in Jarjit settings
  - In Jarjit, go to the Settings menu on the top right and enter the token you received from GitHub into the text field like so: <br>
  <br>
  <picture>
	<img src="assets/set_openai_api_key.png" align="middle" alt="Set API key in settings" width="400">
  </picture><br>
  <br>

- After setting the API key for the first time you'll need to restart the app.

</details>

<details>
    <summary><b>Optional: Setup Multiple API Keys</b></summary>

- Jarjit supports using multiple GitHub API keys to handle rate limiting
- You can add multiple keys in the `api_keys.json` file in the following format:
  ```json
  [
    "your-github-token-1",
    "your-github-token-2"
  ]
  ```
- The app will automatically rotate between keys if rate limits are hit
- You will need to restart the app after these changes.

</details>

<hr>

### <ins>Stuff It's Bad At (For Now)</ins> 😬

- Accurate spatial-reasoning and hence clicking buttons.
- Keeping track of itself in tabular contexts, like Excel and Google Sheets, for similar reasons as stated above.
- Navigating complex GUI-rich applications like Counter-Strike, Spotify, Garage Band, etc due to heavy reliance on cursor actions.


### <ins>Future</ins> 🔮
(*with better models trained on video walkthroughs like Youtube tutorials*)
- "Create a couple of bass samples for me in Garage Band for my latest project."
- "Read this design document for a new feature, edit the code on Github, and submit it for review."
- "Find my friends' music taste from Spotify and create a party playlist for tonight's event."
- "Take the pictures from my Tahoe trip and make a White Lotus type montage in iMovie."

### <ins>Notes</ins> 📝
- Cost: Free! Uses GitHub's API with generous rate limits
- You can interrupt the app anytime by pressing the Stop button, or by dragging your cursor to any of the screen corners.
- Jarjit can only see your primary display when using multiple monitors. Therefore, if the cursor/focus is on a secondary screen, it might keep retrying the same actions as it is unable to see its progress (especially in MacOS with launching Spotlight).

<hr>

### <ins>System Diagram</ins> 🖼️