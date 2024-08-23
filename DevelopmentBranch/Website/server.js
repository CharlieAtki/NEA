const express = require('express');
const cors = require('cors');
const bcrypt = require('bcrypt');
const fs = require('fs');
const path = require('path');

// 'app' initialises the Express application
const app = express();
// 'port' Defines the port on which the server will listen
const port = 3000;

// CORS is a middleware that allows the server to respond to requests from different origins. This enables cross-origin recourse sharing.
// Applies CORS middleware to allow cross-origin requests
app.use(cors());
// Applies middleware to parse incoming JSON requests
app.use(express.json());

// Endpoint to handle login
// This is a POST route at '/login' where the logic is handled.
// within the HTML file the program addresses -  const response = await fetch('http://localhost:3000/login')
// This is why the path is '/login'
// The route expects a JSON payload with 'username' and 'password' fields in the request body.
app.post('/login', async (req, res) => {
    const { username, password } = req.body;

    console.log(`Received login attempt for username: ${username}`);

    // fs is a built-in Node.js module used to interact with the file system, allowing the program to read and write files
    // This reads the 'users.json' file, which contains the user's data.
    // It uses 'path.join' to safely construct the file path relative to the current directory ('__dirname').
    // If there's an error reading the file, a server error is returned
    fs.readFile(path.join(__dirname, 'users.json'), 'utf8', async (err, data) => {
        if (err) {
            console.error('Error reading users.json:', err);
            res.status(500).json({ success: false, message: 'Server error while reading user data' });
            return;
        }

        try {
            // The file consent is parsed from JSON into a JS object
            // It then searches for a user in the parsed data with a matching username
            const users = JSON.parse(data);
            const user = users.find(user => user.username === username);

            if (user) {
                // If the user is found, the entered password is compared against the stored hashed password using 'bcrypt.compare'.
                // If the password matches, a success message is returned. Otherwise, an incorrect message is sent back
                const match = await bcrypt.compare(password, user.password_hash);
                // if the user is not found or the password does not match, appropriate error messages are returned.
                if (match) {
                    res.json({ success: true, message: 'Login successful' });
                } else {
                    res.json({ success: false, message: 'Incorrect password' });
                }
            } else {
                res.json({ success: false, message: 'User not found' });
            }
        // Errors in parsing or reading the user data are caught and logged, with a corresponding server error response send back
        } catch (parseError) {
            console.error('Error parsing users.json:', parseError);
            res.status(500).json({ success: false, message: 'Server error while processing user data' });
        }
    });
});

// Finally, the server starts and listens on the specific port (3000), logging a message to the console
app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
});

// Summary:
// This program provides a simple login API endpoint
// that verifies user credentials by comparing the provided password with a hashed password stored in a JSON file.
// It uses Express to handle HTTP requests and responses, bcrypt for secure password handling, and the file system to read user data