
# coding: utf-8

# # TV Script Generation
# In this project, you'll generate your own [Simpsons](https://en.wikipedia.org/wiki/The_Simpsons) TV scripts using RNNs.  You'll be using part of the [Simpsons dataset](https://www.kaggle.com/wcukierski/the-simpsons-by-the-data) of scripts from 27 seasons.  The Neural Network you'll build will generate a new TV script for a scene at [Moe's Tavern](https://simpsonswiki.com/wiki/Moe's_Tavern).
# 
# <img src="assets/moes_bar.jpg" alt="Moe's Tavern"/>
# 
# ## Get the Data
# The data is already provided for you.  You'll be using a subset of the original dataset.  It consists of only the scenes in Moe's Tavern.  This doesn't include other versions of the tavern, like "Moe's Cavern", "Flaming Moe's", "Uncle Moe's Family Feed-Bag", etc..

# In[1]:

"""
DON'T MODIFY ANYTHING IN THIS CELL
"""
import helper

data_dir = './data/simpsons/moes_tavern_lines.txt'
text = helper.load_data(data_dir)
# Ignore notice, since we don't use it for analysing the data
text = text[81:]


# ## Explore the Data
# Play around with `view_sentence_range` to view different parts of the data.

# In[2]:

view_sentence_range = (0, 10)

"""
DON'T MODIFY ANYTHING IN THIS CELL
"""
import numpy as np

print('Dataset Stats')
print('Roughly the number of unique words: {}'.format(len({word: None for word in text.split()})))
scenes = text.split('\n\n')
print('Number of scenes: {}'.format(len(scenes)))
sentence_count_scene = [scene.count('\n') for scene in scenes]
print('Average number of sentences in each scene: {}'.format(np.average(sentence_count_scene)))

sentences = [sentence for scene in scenes for sentence in scene.split('\n')]
print('Number of lines: {}'.format(len(sentences)))
word_count_sentence = [len(sentence.split()) for sentence in sentences]
print('Average number of words in each line: {}'.format(np.average(word_count_sentence)))

print()
print('The sentences {} to {}:'.format(*view_sentence_range))
print('\n'.join(text.split('\n')[view_sentence_range[0]:view_sentence_range[1]]))


# ## Implement Preprocessing Functions
# The first thing to do to any dataset is preprocessing.  Implement the following preprocessing functions below:
# - Lookup Table
# - Tokenize Punctuation
# 
# ### Lookup Table
# To create a word embedding, you first need <b>to transform the words to ids.</b>  In this function, create two dictionaries:
# - Dictionary to go from the words to an id, we'll call `vocab_to_int`
# - Dictionary to go from the id to word, we'll call `int_to_vocab`
# 
# Return these dictionaries in the following tuple `(vocab_to_int, int_to_vocab)`

# In[3]:

import numpy as np
import problem_unittests as tests
from collections import Counter

def create_lookup_tables(text):
    """
    Create lookup tables for vocabulary
    :param text: The text of tv scripts split into words
    :return: A tuple of dicts (vocab_to_int, int_to_vocab)
    """
    ### Too Long change the way to create_lockup_tables
    # Create a counter 
    # A Counter is a container that keeps track of how many times equivalent values are added. 
    # It can be used to implement the same algorithms for which bag or multiset data structures are commonly used in other 
    # languages.
    #counter = Counter(text)
    
    # Sort our vocabulary
    # key parameter to specify a function to be called on each list element prior to making comparisons.
    # reverse = True: sort on primary key, descending
    #sorted_vocab = sorted(counter, key=counter.get, reverse=True)
    
    
    vocab = set(text)
    
    # Dictionary to go from the words to an id, we'll call vocab_to_int
    vocab_to_int = {word: ii for ii, word in enumerate(vocab)}
    
    # Dictionary to go from the id to word, we'll call int_to_vocab
    int_to_vocab = dict(enumerate(vocab))
    
  
    return vocab_to_int, int_to_vocab
    
    
   

"""
DON'T MODIFY ANYTHING IN THIS CELL THAT IS BELOW THIS LINE
"""
tests.test_create_lookup_tables(create_lookup_tables)


# ### Tokenize Punctuation
# We'll be splitting the script into a word array using spaces as delimiters.  However, punctuations like periods and exclamation marks make it hard for the neural network to distinguish between the word "bye" and "bye!".
# 
# Implement the function `token_lookup` to return a dict that will be used to tokenize symbols like "!" into "||Exclamation_Mark||".  Create a dictionary for the following symbols where the symbol is the key and value is the token:
# - Period ( . )
# - Comma ( , )
# - Quotation Mark ( " )
# - Semicolon ( ; )
# - Exclamation mark ( ! )
# - Question mark ( ? )
# - Left Parentheses ( ( )
# - Right Parentheses ( ) )
# - Dash ( -- )
# - Return ( \n )
# 
# This dictionary will be used to token the symbols and add the delimiter (space) around it.  This separates the symbols as it's own word, making it easier for the neural network to predict on the next word. Make sure you don't use a token that could be confused as a word. Instead of using the token "dash", try using something like "||dash||".

# In[4]:

def token_lookup():
    """
    Generate a dict to turn punctuation into a token.
    :return: Tokenize dictionary where the key is the punctuation and the value is the token
    """
    # TODO: Implement Function

    punctuation = {'.': '||Period||', 
                   ',': '||Comma||', 
                   '"': '||Quotation_Mark||',
                   ';': '||Semicolon||',
                   '!': '||Exclamation_Mark||',
                   '?': '||Question_Mark||',
                   '(': '||Left_Parentheses||',
                   ')': '||Right_Parentheses||',
                   '--': '||Dash||',
                   "\n": '||Return||'}  
    
    return punctuation

"""
DON'T MODIFY ANYTHING IN THIS CELL THAT IS BELOW THIS LINE
"""
tests.test_tokenize(token_lookup)


# ## Preprocess all the data and save it
# Running the code cell below will preprocess all the data and save it to file.

# In[5]:

"""
DON'T MODIFY ANYTHING IN THIS CELL
"""
# Preprocess Training, Validation, and Testing Data
helper.preprocess_and_save_data(data_dir, token_lookup, create_lookup_tables)


# # Check Point
# This is your first checkpoint. If you ever decide to come back to this notebook or have to restart the notebook, you can start from here. The preprocessed data has been saved to disk.

# In[6]:

"""
DON'T MODIFY ANYTHING IN THIS CELL
"""
import helper
import numpy as np
import problem_unittests as tests

int_text, vocab_to_int, int_to_vocab, token_dict = helper.load_preprocess()


# ## Build the Neural Network
# You'll build the components necessary to build a RNN by implementing the following functions below:
# - get_inputs
# - get_init_cell
# - get_embed
# - build_rnn
# - build_nn
# - get_batches
# 
# ### Check the Version of TensorFlow and Access to GPU

# In[7]:

"""
DON'T MODIFY ANYTHING IN THIS CELL
"""
from distutils.version import LooseVersion
import warnings
import tensorflow as tf

# Check TensorFlow Version
assert LooseVersion(tf.__version__) >= LooseVersion('1.0'), 'Please use TensorFlow version 1.0 or newer'
print('TensorFlow Version: {}'.format(tf.__version__))

# Check for a GPU
if not tf.test.gpu_device_name():
    warnings.warn('No GPU found. Please use a GPU to train your neural network.')
else:
    print('Default GPU Device: {}'.format(tf.test.gpu_device_name()))


# ### Input
# Implement the `get_inputs()` function to create TF Placeholders for the Neural Network.  It should create the following placeholders:
# - Input text placeholder named "input" using the [TF Placeholder](https://www.tensorflow.org/api_docs/python/tf/placeholder) `name` parameter.
# - Targets placeholder
# - Learning Rate placeholder
# 
# Return the placeholders in the following the tuple `(Input, Targets, LearningRate)`

# In[8]:

def get_inputs():
    """
    Create TF Placeholders for input, targets, and learning rate.
    :return: Tuple (input, targets, learning rate)
    """
    input = tf.placeholder(tf.int32, shape=[None, None], name='input')
    targets = tf.placeholder(tf.int32, shape=[None, None], name='targets')
    learningRate = tf.placeholder(tf.float32,  name='learningRate')
    
    return input, targets, learningRate


"""
DON'T MODIFY ANYTHING IN THIS CELL THAT IS BELOW THIS LINE
"""
tests.test_get_inputs(get_inputs)


# ### Build RNN Cell and Initialize
# 
# <img src="assets/lstm.png" alt="RNN LSTM schema"/>
# 
# Stack one or more [`BasicLSTMCells`](https://www.tensorflow.org/api_docs/python/tf/contrib/rnn/BasicLSTMCell) in a [`MultiRNNCell`](https://www.tensorflow.org/api_docs/python/tf/contrib/rnn/MultiRNNCell).
# - The Rnn size should be set using `rnn_size`
# - Initalize Cell State using the MultiRNNCell's [`zero_state()`](https://www.tensorflow.org/api_docs/python/tf/contrib/rnn/MultiRNNCell#zero_state) function
#     - Apply the name "initial_state" to the initial state using [`tf.identity()`](https://www.tensorflow.org/api_docs/python/tf/identity)
# 
# Return the cell and initial state in the following tuple `(Cell, InitialState)`
# 
# ### From LSTM with TensorFlow Tutorial
# 
# The core of the model consists of an LSTM cell <b>that processes one word at a time and computes probabilities of the possible values for the next word in the sentence.</b>
# <br>
# The memory state of the network is initialized with a vector of zeros and gets updated after reading each word. For computational reasons, we will process data in mini-batches of size batch_size.
# 
# #### Stacking multiple LSTMs
# 
# To give the model more expressive power, we can add multiple layers of LSTMs to process the data. The output of the first layer will become the input of the second and so on.
# 
# We have a class called MultiRNNCell that makes the implementation seamless:
# 

# In[9]:

def get_init_cell(batch_size, rnn_size):
    """
    Create an RNN Cell and initialize it.
    :param batch_size: Size of batches
    :param rnn_size: Size of RNNs
    :return: Tuple (cell, initialize state)
    """
    
    # Add DropoutWrapper to improve our loss.
    layers = 1;
    LSTM = tf.contrib.rnn.BasicLSTMCell(rnn_size)
    Cell = tf.contrib.rnn.MultiRNNCell([LSTM] * layers)

    InitialState = Cell.zero_state(batch_size, tf.float32)
    
     # Initial state of the LSTM memory.
    InitialState = tf.identity(InitialState, name="initial_state")
            
    return Cell, InitialState



"""
DON'T MODIFY ANYTHING IN THIS CELL THAT IS BELOW THIS LINE
"""
tests.test_get_init_cell(get_init_cell)


# ### Word Embedding
# Apply embedding to `input_data` using TensorFlow.  Return the embedded sequence.
# 
# #### A reminder about Word Embedding
# When you're dealing with language and words, you end up with tens of thousands of classes to predict, one for each word. Trying to one-hot encode these words is massively inefficient, you'll have one element set to 1 and the other 50,000 set to 0. The word2vec algorithm finds much more efficient representations by finding vectors that represent the words. These vectors also contain semantic information about the words. Words that show up in similar contexts, such as "black", "white", and "red" will have vectors near each other. There are two architectures for implementing word2vec, CBOW (Continuous Bag-Of-Words) and Skip-gram.
# 
# 
# Embeddings is a deep neural network method for representing data <b> with a huge nb of classes more efficiently </b>
# 

# In[10]:

def get_embed(input_data, vocab_size, embed_dim):
    """
    Create embedding for <input_data>.
    :param input_data: TF placeholder for text input.
    :param vocab_size: Number of words in vocabulary.
    :param embed_dim: Number of embedding dimensions
    :return: Embedded input.
    """
    
    # Define our embedding matrix :
    # Just a big random matrix to start : initialize the values to be uniform in the unit cube.
    embedding = tf.Variable(tf.random_uniform([vocab_size, embed_dim], -1.0, 1.0))
    
    # Now what we need to do is look up the vector for each of the source words in the batch. 
    # TensorFlow has handy helpers that make this easy : use tf.nn.embedding_lookup to get the hidden layer output
    embed = tf.nn.embedding_lookup(embedding, input_data)

    return embed


"""
DON'T MODIFY ANYTHING IN THIS CELL THAT IS BELOW THIS LINE
"""
tests.test_get_embed(get_embed)


# ### Build RNN
# You created a RNN Cell in the `get_init_cell()` function.  Time to use the cell to create a RNN.
# - Build the RNN using the [`tf.nn.dynamic_rnn()`](https://www.tensorflow.org/api_docs/python/tf/nn/dynamic_rnn)
#  - Apply the name "final_state" to the final state using [`tf.identity()`](https://www.tensorflow.org/api_docs/python/tf/identity)
# 
# Return the outputs and final_state state in the following tuple `(Outputs, FinalState)` 

# In[11]:

def build_rnn(cell, inputs):
    """
    Create a RNN using a RNN Cell
    :param cell: RNN Cell
    :param inputs: Input text data
    :return: Tuple (Outputs, Final State)
    """
    #Outputs = tf.nn.dynamic_rnn(cell, inputs)
    #FinalState = tf.identity(output)
        
    Outputs, FinalState = tf.nn.dynamic_rnn(cell, inputs, dtype=tf.float32) 
    FinalState = tf.identity(FinalState, name="final_state")

    return Outputs, FinalState


"""
DON'T MODIFY ANYTHING IN THIS CELL THAT IS BELOW THIS LINE
"""
tests.test_build_rnn(build_rnn)


# ### Build the Neural Network
# Apply the functions you implemented above to:
# - Apply embedding to `input_data` using your `get_embed(input_data, vocab_size, embed_dim)` function.
# - Build RNN using `cell` and your `build_rnn(cell, inputs)` function.
# - Apply a fully connected layer with a linear activation and `vocab_size` as the number of outputs.
# 
# Return the logits and final state in the following tuple (Logits, FinalState) 

# In[12]:

def build_nn(cell, rnn_size, input_data, vocab_size):
    """
    Build part of the neural network
    :param cell: RNN cell
    :param rnn_size: Size of rnns
    :param input_data: Input data
    :param vocab_size: Vocabulary size
    :return: Tuple (Logits, FinalState)
    """
    
    # Apply embedding to input_data using your get_embed(input_data, vocab_size, embed_dim) function.
    embed = get_embed(input_data, vocab_size, rnn_size)
    
    # Build RNN using cell and your build_rnn(cell, inputs) function.
    Outputs, FinalState = build_rnn(cell, embed)
    
    # Apply a fully connected layer with a linear activation (so default:None) and vocab_size as the number of outputs.
    Logits = tf.contrib.layers.fully_connected(Outputs, vocab_size, weights_initializer = tf.truncated_normal_initializer(stddev=0.01),
                                               biases_initializer = tf.zeros_initializer(), activation_fn=None)
    
    # TODO: Implement Function
    return Logits, FinalState




"""
DON'T MODIFY ANYTHING IN THIS CELL THAT IS BELOW THIS LINE
"""
tests.test_build_nn(build_nn)


# ### Batches
# Implement `get_batches` to create batches of input and targets using `int_text`.  The batches should be a Numpy array with the shape `(number of batches, 2, batch size, sequence length)`. Each batch contains two elements:
# - The first element is a single batch of **input** with the shape `[batch size, sequence length]`
# - The second element is a single batch of **targets** with the shape `[batch size, sequence length]`
# 
# If you can't fill the last batch with enough data, drop the last batch.
# 
# For exmple, `get_batches([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], 2, 3)` would return a Numpy array of the following:
# ```
# [
#   # First Batch
#   [
#     # Batch of Input
#     [[ 1  2  3], [ 7  8  9]],
#     # Batch of targets
#     [[ 2  3  4], [ 8  9 10]]
#   ],
#  
#   # Second Batch
#   [
#     # Batch of Input
#     [[ 4  5  6], [10 11 12]],
#     # Batch of targets
#     [[ 5  6  7], [11 12 13]]
#   ]
# ]
# ```

# In[13]:

def get_batches(int_text, batch_size, seq_length):
    """
    Return batches of input and target
    :param int_text: Text with the words replaced by their ids
    :param batch_size: The size of batch
    :param seq_length: The length of sequence
    :return: Batches as a Numpy array
    """
    n_elements = len(int_text)
    n_batches = n_elements // (batch_size * seq_length)
    
    xdata = np.array(int_text[: n_batches * batch_size * seq_length])
    ydata = np.array(int_text[1: n_batches * batch_size * seq_length + 1])
    
    x_batches = np.split(xdata.reshape(batch_size, -1), n_batches, 1)
    y_batches = np.split(ydata.reshape(batch_size, -1), n_batches, 1)
    
    Batches = np.array(list(zip(x_batches, y_batches)))

    return Batches


"""
DON'T MODIFY ANYTHING IN THIS CELL THAT IS BELOW THIS LINE
"""
tests.test_get_batches(get_batches)


# ## Neural Network Training
# ### Hyperparameters
# Tune the following parameters:
# 
# - Set `num_epochs` to the number of epochs.
# - Set `batch_size` to the batch size.
# - Set `rnn_size` to the size of the RNNs.
# - Set `seq_length` to the length of sequence.
# - Set `learning_rate` to the learning rate.
# - Set `show_every_n_batches` to the number of batches the neural network should print progress.

# In[14]:

# Number of Epochs
num_epochs = 50
# Batch Size
batch_size = 256
# RNN Size
rnn_size = 1024
# Sequence Length
seq_length = 25
# Learning Rate
learning_rate = 0.006
# Show stats for every n number of batches
show_every_n_batches = 60

"""
DON'T MODIFY ANYTHING IN THIS CELL THAT IS BELOW THIS LINE
"""
save_dir = './save'


# ### Build the Graph
# Build the graph using the neural network you implemented.

# In[15]:

"""
DON'T MODIFY ANYTHING IN THIS CELL
"""
from tensorflow.contrib import seq2seq

train_graph = tf.Graph()
with train_graph.as_default():
    vocab_size = len(int_to_vocab)
    input_text, targets, lr = get_inputs()
    input_data_shape = tf.shape(input_text)
    cell, initial_state = get_init_cell(input_data_shape[0], rnn_size)
    logits, final_state = build_nn(cell, rnn_size, input_text, vocab_size)

    # Probabilities for generating words
    probs = tf.nn.softmax(logits, name='probs')

    # Loss function
    cost = seq2seq.sequence_loss(
        logits,
        targets,
        tf.ones([input_data_shape[0], input_data_shape[1]]))

    # Optimizer
    optimizer = tf.train.AdamOptimizer(lr)

    # Gradient Clipping
    gradients = optimizer.compute_gradients(cost)
    capped_gradients = [(tf.clip_by_value(grad, -1., 1.), var) for grad, var in gradients]
    train_op = optimizer.apply_gradients(capped_gradients)


# ## Train
# Train the neural network on the preprocessed data.  If you have a hard time getting a good loss, check the [forms](https://discussions.udacity.com/) to see if anyone is having the same problem.

# In[16]:

"""
DON'T MODIFY ANYTHING IN THIS CELL
"""
batches = get_batches(int_text, batch_size, seq_length)

with tf.Session(graph=train_graph) as sess:
    sess.run(tf.global_variables_initializer())

    for epoch_i in range(num_epochs):
        state = sess.run(initial_state, {input_text: batches[0][0]})

        for batch_i, (x, y) in enumerate(batches):
            feed = {
                input_text: x,
                targets: y,
                initial_state: state,
                lr: learning_rate}
            train_loss, state, _ = sess.run([cost, final_state, train_op], feed)

            # Show every <show_every_n_batches> batches
            if (epoch_i * len(batches) + batch_i) % show_every_n_batches == 0:
                print('Epoch {:>3} Batch {:>4}/{}   train_loss = {:.3f}'.format(
                    epoch_i,
                    batch_i,
                    len(batches),
                    train_loss))

    # Save Model
    saver = tf.train.Saver()
    saver.save(sess, save_dir)
    print('Model Trained and Saved')


# In[17]:

"""
DON'T MODIFY ANYTHING IN THIS CELL
"""
# Save parameters for checkpoint
helper.save_params((seq_length, save_dir))


# # Checkpoint

# In[18]:

"""
DON'T MODIFY ANYTHING IN THIS CELL
"""
import tensorflow as tf
import numpy as np
import helper
import problem_unittests as tests

_, vocab_to_int, int_to_vocab, token_dict = helper.load_preprocess()
seq_length, load_dir = helper.load_params()


# ## Implement Generate Functions
# ### Get Tensors
# Get tensors from `loaded_graph` using the function [`get_tensor_by_name()`](https://www.tensorflow.org/api_docs/python/tf/Graph#get_tensor_by_name).  Get the tensors using the following names:
# - "input:0"
# - "initial_state:0"
# - "final_state:0"
# - "probs:0"
# 
# Return the tensors in the following tuple `(InputTensor, InitialStateTensor, FinalStateTensor, ProbsTensor)` 

# In[19]:

def get_tensors(loaded_graph):
    """
    Get input, initial state, final state, and probabilities tensor from <loaded_graph>
    :param loaded_graph: TensorFlow graph loaded from file
    :return: Tuple (InputTensor, InitialStateTensor, FinalStateTensor, ProbsTensor)
    """
    InputTensor = loaded_graph.get_tensor_by_name("input:0")
    InitialStateTensor = loaded_graph.get_tensor_by_name("initial_state:0")
    FinalStateTensor = loaded_graph.get_tensor_by_name("final_state:0")
    ProbsTensor = loaded_graph.get_tensor_by_name("probs:0")
    
    return InputTensor, InitialStateTensor, FinalStateTensor, ProbsTensor


"""
DON'T MODIFY ANYTHING IN THIS CELL THAT IS BELOW THIS LINE
"""
tests.test_get_tensors(get_tensors)


# ## Save Parameters
# Save `seq_length` and `save_dir` for generating a new TV script.

# ### Choose Word
# Implement the `pick_word()` function to select the next word using `probabilities`.

# In[20]:

def pick_word(probabilities, int_to_vocab):
    """
    Pick the next word in the generated text
    :param probabilities: Probabilites of the next word
    :param int_to_vocab: Dictionary of word ids as the keys and words as the values
    :return: String of the predicted word
    """
    p = np.argmax(probabilities)
    return int_to_vocab[p]


"""
DON'T MODIFY ANYTHING IN THIS CELL THAT IS BELOW THIS LINE
"""
tests.test_pick_word(pick_word)


# ## Generate TV Script
# This will generate the TV script for you.  Set `gen_length` to the length of TV script you want to generate.

# In[21]:

gen_length = 200
# homer_simpson, moe_szyslak, or Barney_Gumble
prime_word = 'moe_szyslak'

"""
DON'T MODIFY ANYTHING IN THIS CELL THAT IS BELOW THIS LINE
"""
loaded_graph = tf.Graph()
with tf.Session(graph=loaded_graph) as sess:
    # Load saved model
    loader = tf.train.import_meta_graph(load_dir + '.meta')
    loader.restore(sess, load_dir)

    # Get Tensors from loaded model
    input_text, initial_state, final_state, probs = get_tensors(loaded_graph)

    # Sentences generation setup
    gen_sentences = [prime_word + ':']
    prev_state = sess.run(initial_state, {input_text: np.array([[1]])})

    # Generate sentences
    for n in range(gen_length):
        # Dynamic Input
        dyn_input = [[vocab_to_int[word] for word in gen_sentences[-seq_length:]]]
        dyn_seq_length = len(dyn_input[0])

        # Get Prediction
        probabilities, prev_state = sess.run(
            [probs, final_state],
            {input_text: dyn_input, initial_state: prev_state})
        
        pred_word = pick_word(probabilities[dyn_seq_length-1], int_to_vocab)

        gen_sentences.append(pred_word)
    
    # Remove tokens
    tv_script = ' '.join(gen_sentences)
    for key, token in token_dict.items():
        ending = ' ' if key in ['\n', '(', '"'] else ''
        tv_script = tv_script.replace(' ' + token.lower(), key)
    tv_script = tv_script.replace('\n ', '\n')
    tv_script = tv_script.replace('( ', '(')
        
    print(tv_script)


# # The TV Script is Nonsensical
# It's ok if the TV script doesn't make any sense.  We trained on less than a megabyte of text.  In order to get good results, you'll have to use a smaller vocabulary or get more data.  Luckly there's more data!  As we mentioned in the begging of this project, this is a subset of [another dataset](https://www.kaggle.com/wcukierski/the-simpsons-by-the-data).  We didn't have you train on all the data, because that would take too long.  However, you are free to train your neural network on all the data.  After you complete the project, of course.
# # Submitting This Project
# When submitting this project, make sure to run all the cells before saving the notebook. Save the notebook file as "dlnd_tv_script_generation.ipynb" and save it as a HTML file under "File" -> "Download as". Include the "helper.py" and "problem_unittests.py" files in your submission.
