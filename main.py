from flask import Flask, request, session, g, make_response, flash, render_template, redirect, url_for, jsonify

app = Flask(__name__)
app.config['SECRET_KEY']='xxx'

def multiple_replace(original,substitution,seq):
    return ''.join([dict(zip(original,substitution)).get(x,x) for x in seq])

def diff_str(seq1,seq2):
    n = 0
    for i in zip(seq1, seq2):
        if i[0] != i[1]:
            n += 1
    return n

def palindromic_find(sequence, len_tuple, gap_tuple, threshold):
    seq_list = []
    for i in range(len(sequence)):
        for j in range(len_tuple[0],len_tuple[1]+1):
            lin = ''.join(list(reversed(list(multiple_replace(['A','T','C','G'], ['T','A','G','C'], sequence[i:i+j])))))
            for k in range(gap_tuple[0], gap_tuple[1]+1):
                if len(sequence[i+j+k:i+j+k+j])==len(lin) and diff_str(sequence[i+j+k:i+j+k+j], lin) <= threshold:
                    seq_list.append((str(i+1)+' '+sequence[i:i+j]+'-'*(k)+sequence[i+j+k:i+j+k+j]+' '+str(i+j+k+j), list(range(i+1, i+1+j))+list(range(i+j+k+1, i+j+j+k+1))))
    return seq_list

@app.route('/')
def index():
    return render_template('index')

@app.route('/ajaxdata', methods=['POST'])
def ajaxdata():
    return jsonify({'data': palindromic_find(request.form['sequence'], (int(request.form['minlen']), int(request.form['maxlen'])), (int(request.form['mingap']), int(request.form['maxgap'])), int(request.form['threshold']))})

if __name__ == '__main__':
    app.run(debug=True)