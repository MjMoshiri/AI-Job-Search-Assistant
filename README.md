<div align="center">
  <h1>Job Search Assistant</h1>
  <br>
  <img src="image.png" width="300" height="300">
  <br><br>
   <br>
</div>  <br>


 This tool helps automate the job search by fetching job listings, filtering them based on specific criteria, and displaying qualified job opportunities using an interface. <a href="https://www.linkedin.com/feed/update/urn:li:activity:7197691328757919744/">Original Post</a>

## Components

- **/db**: Contains the main database. Direct access to the database is restricted.
- **/db API**: A Python API to access the database securely.
- **/.env**: Configuration file that must be set up with the following environment variables:
    - POSTGRES_USER
    - POSTGRES_PASSWORD
    - POSTGRES_DB
    - OPENAI_API_KEY

- **Docker**: Utilizes Docker to run the database. Ensure Docker is installed and use the command:
    ```bash
    docker compose build
    ```
to start the database.

- **/indeed-scrapper**: An exemplary scrapper that fetches job data. Future updates might include additional scrapers for other platforms.

- **/qualification-checker**: A Python script that uses the OpenAI API to determine if a job listing qualifies under the specified criteria.

- **/ui**: A React-based UI that displays the jobs that qualify under the specified criteria.

## Setup

To get started, clone this repository and ensure Docker is installed on your machine. Set up the `.env` file with the necessary credentials and tokens. Then, run the following command to start the database:

```bash
docker compose up
```

Other components can be run independently. For example, to run the qualification checker, use the following command:

```bash
python qualification-checker/app.py
```

To run the UI, navigate to the `ui` directory and run the following command:

```bash
npm start
```

## License

This project is licensed under a permissive license that allows usage and modification as long as credit is given to the original creator. 

Happy coding, and best of luck with your job searches!
