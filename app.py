from flask import Flask, render_template, request, jsonify
import numpy as np

app = Flask(__name__)

# Initialize a random cellular automata
data = np.zeros((1, 1), dtype=int)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/init', methods=['POST'])
def init():
    global data
    
    window_size = request.get_json()
    # Initialize a random cellular automata based on the window size
    data = np.zeros((int(window_size['height']/20), int(window_size['width']/20)), dtype=int)
    print(window_size)
    #data = np.zeros((50, 100), dtype=int)
    #data[1, 1] = 1
    #data[25, 26] = 1
    #data[25, 27] = 1
    #data[25, 28] = 1
    # Return the initial state of the cellular automata
    return jsonify(data.tolist())

@app.route('/update', methods=['POST'])
def update():
    global data
    # Get the state of each cell as set by the user
    user_data = request.get_json()
    if user_data is not None:
        data = np.array(request.get_json(), dtype=int)
    # Update the cellular automata
    data = update_data(data)
    return jsonify(data.tolist())


def update_data(data):
    # Create a new array to hold the next state
    next_state = np.zeros(data.shape, dtype=int)

    # Iterate over each cell
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            # Count the cell's eight neighbors
            total = (data[i, (j-1)%data.shape[1]] + data[i, (j+1)%data.shape[1]] +
                     data[(i-1)%data.shape[0], j] + data[(i+1)%data.shape[0], j] +
                     data[(i-1)%data.shape[0], (j-1)%data.shape[1]] + data[(i-1)%data.shape[0], (j+1)%data.shape[1]] +
                     data[(i+1)%data.shape[0], (j-1)%data.shape[1]] + data[(i+1)%data.shape[0], (j+1)%data.shape[1]])

            # Apply the Game of Life rules
            if data[i, j] == 1:
                if total < 2 or total > 3:
                    next_state[i, j] = 0
                else:
                    next_state[i, j] = 1
            else:
                if total == 3:
                    next_state[i, j] = 1

    return next_state

if __name__ == '__main__':
    app.run(debug=True)
