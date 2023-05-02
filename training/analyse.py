from subprocess import Popen, PIPE, STDOUT, TimeoutExpired
import pandas as pd
import re

def ecommand(p, comm):
    p.stdin.write(f'{comm}\n')

#Create subprocess for to run lc0
def open_engine():
    #Replace the path with your own
    p = Popen([r'C:\Users\Marceli\leela_chess_zero\lc0-v0.28.2-windows-gpu-opencl\lc0.exe'], stdout=PIPE, stdin=PIPE, stderr=STDOUT, bufsize=0, text=True)
    return p

#Kill the process once the analysis is complete
def close_engine(p):
    ecommand(p, 'quit') 
    try:
        p.communicate(timeout=5)
    except TimeoutExpired: 
        p.kill()
        p.communicate()


def analyse(p, position, nodes):
    #Set lc0 options
    ecommand(p, 'setoption name verbosemovestats value true')
    ecommand(p, f'position fen {position}')
    ecommand(p, f'go nodes {nodes} multipv 5')
    all_values = []
    all_moves = []
    all_features = ['P', 'W', 'D', 'M', 'Q', 'U', 'S', 'V']
    #Read through lc0 output
    for line in iter(p.stdout.readline, ''):  
        line = line.strip()
        if line.startswith('info string'):
            values = []
            for elem in re.findall(r'\(.*?\)', line)[2:]:
                if not elem=="(T)": 
                    feature, value = elem.split()
                    feature, value = feature[1], value[:-1]
                    if feature == 'P':
                        value = value[:-1]
                        value = round(float(value),2)
                    else: 
                        try: 
                            value = float(value)
                        except:
                            value = None
                    values.append(value)
                
            move = line.split()[2]
            all_moves.append(move)
            all_values.append(values.copy())
        
        if line.startswith('bestmove'):  # exit the loop when we get the engine bestmove  
            break
        
    df = pd.DataFrame(all_values, columns=all_features, index=all_moves)
    df.drop(df.tail(1).index,inplace=True) # drop last row
    df = df.sort_values(by="V", ascending = False)
    df = df[['V']]
    return df