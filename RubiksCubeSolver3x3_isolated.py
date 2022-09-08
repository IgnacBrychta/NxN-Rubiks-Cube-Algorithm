from tkinter import *
import time
from copy import deepcopy
import random
from os import system
system('cls')
session = "5x5"
SIDE_LENGTH = 5
root = Tk()
logo_sticker = "YJ.jpg"
frame = LabelFrame(root,bd=5,width=1,height=1)
frame.grid(row=2,column=2,columnspan=4)
frame.grid_propagate(False)
def visualize(input_scramble,available_turns):
    global cube_nxn,SIDE_LENGTH,visualization,buttons_root,moves_done,undone_moves,root,cube_nxn_solved,scramble
    turns = available_turns
    scramble = input_scramble
    reverse_translation={str(SIDE_LENGTH)+"L'": "R", str(SIDE_LENGTH)+'L': "R'", str(SIDE_LENGTH)+'L2': 'R2', str(SIDE_LENGTH)+"U'": 'D', str(SIDE_LENGTH)+"U": "D'", str(SIDE_LENGTH)+'U2': 'D2', str(SIDE_LENGTH)+"F'": 'B', str(SIDE_LENGTH)+'F': "B'", str(SIDE_LENGTH)+'F2': 'B2'}
    moves_done=[]
    undone_moves=[]
    o = "Orange"
    r = "Red"
    g = "Green"
    b = "Blue"
    y = "Yellow"
    w = "White"
    TOP_FACE = 0
    LEFT_FACE = 1
    FRONT_FACE = 2
    RIGHT_FACE = 3
    BACK_FACE = 4
    BOTTOM_FACE = 5
    # Algoritmus na složení 3x3
    def find_a_solution():
        print(f"\n\n\n\n\nAlgorithm Start\nScramble: {scramble}\n\n\n\n\n")
        global cube_nxn,cube_nxn_solved,algorithm_solution,simplified_solution
        simplified_solution=[]
        algorithm_solution=[]
        # Funkce pro aplikování vygenerovaného pohybu
        def add_move_to_solution(move):
            global algorithm_solution,cube_nxn,moves_done
            if 0:
                moves_done.append(move)
            algorithm_solution.append(move)
            do_move(move,show=False)
        # Nebude fungovat, když bude kostka natočena jinak, než W navrchu a Y zespodu
        # Srovnání kostky - w nahoře, r vepředu
        center=round((SIDE_LENGTH**2)/2)
        CUBE_COLORS = [w, g, r, b, o, y]
        CENTER_LINE = SIDE_LENGTH//2+1
        ROTATION_NOTATION_FOR_FACES = {
            0: "U",
            1: "L",
            2: "F",
            3: f"{SIDE_LENGTH}L",
            4: f"{SIDE_LENGTH}F",
            5: f"{SIDE_LENGTH}U"
        }
        def CountLineCompletion(face: int, line: int, color: str) -> int:
            colorOnFaceCount = 0
            for piece in range(line*SIDE_LENGTH + 1, (line + 1)*SIDE_LENGTH - 1):
                if cube_nxn[face][piece] == color and piece != center:
                    colorOnFaceCount += 1
            return colorOnFaceCount
            
        def SumOfColorsOnFace(face: int) -> int:
            countOfFaceCenterColor = 0
            for line_horizontal in range(1, SIDE_LENGTH-1):
                for piece in range(line_horizontal*SIDE_LENGTH + 1, (line_horizontal + 1)*SIDE_LENGTH - 1):
                    if cube_nxn[face][piece] == cube_nxn[face][center]:
                        countOfFaceCenterColor+=1
            return countOfFaceCenterColor
            #for move in ["U", f"{SIDE_LENGTH}U", "F", f"{SIDE_LENGTH}F", "L", f"{SIDE_LENGTH}L"]:
            #    add_move_to_solution(move)
        def FindMostCommonColorOnFace(colorCount: dict) -> str:
            mostCommonColor = [w, 0]
            for color, count in colorCount.items():
                if count > mostCommonColor[1]:
                    mostCommonColor = [color, count]
            return mostCommonColor
        def ReduceCubeAlgorithm():
            def ChooseStartingFace():
                countsOfMovesCommonColorsOnFaces = {
                    0: 0,
                    1: 0,
                    2: 0,
                    3: 0,
                    4: 0,
                    5: 0
                }
                for face in countsOfMovesCommonColorsOnFaces.keys():
                    countsOfMovesCommonColorsOnFaces[face] = SumOfColorsOnFace(face)
                startingFace = max(countsOfMovesCommonColorsOnFaces.items(), key=lambda x: x[1])[0]
                print(f"{countsOfMovesCommonColorsOnFaces=}")
                print(f"{startingFace=}")
                return startingFace
            startingFace = ChooseStartingFace()
            colorOfStartingSide = cube_nxn[startingFace][center]
            print(f"{colorOfStartingSide=}")
            def SetCubeToDefaultPositionForSolving():
                while cube_nxn[0][center]!=colorOfStartingSide and cube_nxn[2][center]!=colorOfStartingSide and cube_nxn[5][center]!=colorOfStartingSide:
                    add_move_to_solution("y")
                while cube_nxn[0][center]!=colorOfStartingSide:
                    add_move_to_solution("x")
                add_move_to_solution("x")
            SetCubeToDefaultPositionForSolving()
            ### changed
            def FindMostSolvedLineOnFace(face: int, lineColor: str, line: int) -> None:
                line -= 1
                print("FindMostSolvedLineOnFace()")
                mostSolvedLinesOnDifferentRotations = {
                    0: 0,
                    1: 0,
                    2: 0,
                    3: 0
                }
                for rotation in range(4):
                    for piece in range(line*SIDE_LENGTH + 1, (line + 1)*SIDE_LENGTH - 1):
                        if cube_nxn[face][piece] == lineColor:
                            mostSolvedLinesOnDifferentRotations[rotation] += 1
                    add_move_to_solution(ROTATION_NOTATION_FOR_FACES[face])
                mostSolvedLine_Rotation = max(mostSolvedLinesOnDifferentRotations, key=mostSolvedLinesOnDifferentRotations.get)
                mostSolvedLine_Rotation_color = mostSolvedLinesOnDifferentRotations[mostSolvedLine_Rotation]

                def CountPiecesOnLine():
                    alreadySolvedPiecesOnCurrentLine_ = 0
                    for piece in range(line*SIDE_LENGTH + 1, (line + 1)*SIDE_LENGTH - 1):
                        if cube_nxn[face][piece] == lineColor:
                            alreadySolvedPiecesOnCurrentLine_ += 1
                    return alreadySolvedPiecesOnCurrentLine_
                
                for _ in range(4):
                    alreadySolvedPiecesOnCurrentLine = CountPiecesOnLine()
                    if alreadySolvedPiecesOnCurrentLine != mostSolvedLine_Rotation_color:
                        add_move_to_solution(ROTATION_NOTATION_FOR_FACES[face])
                    else:
                        break
                        
            def SolveLine(solvedFace: int, lineInProgress: int, invertPush: False) -> None:
                line = lineInProgress
                def InvertResult(boolean: bool) -> bool:
                    #print(f"{boolean=}")
                    return False if boolean else True
                def PushLine():
                    print("PushLine()")
                    add_move_to_solution(f"{line}L")
                    if line == CENTER_LINE:
                        add_move_to_solution("U")
                    elif line < CENTER_LINE:
                        add_move_to_solution("U2")
                        add_move_to_solution(f"{line}L'")
                        add_move_to_solution("U")
                    else:
                        add_move_to_solution("U2")
                        add_move_to_solution(f"{line}L'")
                        add_move_to_solution("U'")
                def SolvePushedLine():
                    inverted = False
                    print("SolvePushedLine()")
                    
                    def TrySolveLineUsingFrontFace():
                        print("TrySolveLineUsingFrontFace()")
                        for _ in range(4):
                            add_move_to_solution(ROTATION_NOTATION_FOR_FACES[FRONT_FACE])
                            if cube_nxn[FRONT_FACE][piece] == colorOfStartingSide:
                                add_move_to_solution(f"{line}L'")
                                result = line < CENTER_LINE
                                result = InvertResult(result) if invertPush else result
                                if result:
                                    add_move_to_solution("U")
                                    add_move_to_solution(f"{line}L")
                                    add_move_to_solution("U'")
                                else:
                                    add_move_to_solution("U'")
                                    add_move_to_solution(f"{line}L")
                                    add_move_to_solution("U")
                                break
                            
                    def TrySolveLineUsingBottomFace():
                        print("TrySolveLineUsingBottomFace()")
                        for _ in range(4):
                            add_move_to_solution(ROTATION_NOTATION_FOR_FACES[BOTTOM_FACE])
                            if cube_nxn[BOTTOM_FACE][piece] == colorOfStartingSide:
                                add_move_to_solution(f"{line}L2")
                                if line < CENTER_LINE:
                                    add_move_to_solution("U")
                                    add_move_to_solution(f"{line}L2")
                                    add_move_to_solution("U'")
                                else:
                                    add_move_to_solution("U'")
                                    add_move_to_solution(f"{line}L2")
                                    add_move_to_solution("U")
                                break
                    
                    def TrySolveLineUsingBackFace(): 
                        print("TrySolveLineUsingBackFace()")
                        for _ in range(4):
                            add_move_to_solution(ROTATION_NOTATION_FOR_FACES[BACK_FACE])
                            if cube_nxn[BACK_FACE][piece] == colorOfStartingSide:
                                add_move_to_solution(f"{line}L")
                                if line < CENTER_LINE:
                                    add_move_to_solution("U")
                                    add_move_to_solution(f"{line}L'")
                                    add_move_to_solution("U'")
                                else:
                                    add_move_to_solution("U'")
                                    add_move_to_solution(f"{line}L'")
                                    add_move_to_solution("U")
                                break
                    ### invertPush??
                    ### line_horizontal
                    def TrySolveLineUsingTopFace():
                        
                        print("TrySolveLineUsingTopFace()")
                        # Move lines potentially containing required pieces from the top face to the front face, then solve top using front
                        if lineInProgress != CENTER_LINE:
                            """
                            result = line < CENTER_LINE
                            result = InvertResult(result) if invertPush else result
                            """
                            if not invertPush:
                                if line < CENTER_LINE:
                                    add_move_to_solution("U")
                                    add_move_to_solution(f"{line}L")
                                    add_move_to_solution("F2")
                                    add_move_to_solution(f"{line}L'")
                                    add_move_to_solution("U'")
                                else:
                                    add_move_to_solution("U'")
                                    add_move_to_solution(f"{line}L")
                                    add_move_to_solution("F2")
                                    add_move_to_solution(f"{line}L'")
                                    add_move_to_solution("U")
                                TrySolveLineUsingFrontFace()
                            else:
                                add_move_to_solution("U")
                                add_move_to_solution(f"{CENTER_LINE}L")
                                add_move_to_solution("F")
                                add_move_to_solution(f"{CENTER_LINE}L'")
                                add_move_to_solution("U'")
                                TrySolveLineUsingFrontFace()
                                print("[R]TrySolveLineUsingTopFace()")
                                if cube_nxn[TOP_FACE][piece] != colorOfStartingSide:
                                    add_move_to_solution("U")
                                    for line_BetweenSolvedLineAndCenterLine in range(line+1, CENTER_LINE):
                                        add_move_to_solution(F"{line_BetweenSolvedLineAndCenterLine}L")
                                    add_move_to_solution("F2")
                                    for line_BetweenSolvedLineAndCenterLine in range(line+1, CENTER_LINE):
                                        add_move_to_solution(F"{line_BetweenSolvedLineAndCenterLine}L'")

                                    for line_BetweenCenterLineAndRight in range(CENTER_LINE+1, SIDE_LENGTH):
                                        add_move_to_solution(F"{line_BetweenCenterLineAndRight}L")
                                    add_move_to_solution("F2")
                                    for line_BetweenCenterLineAndRight in range(CENTER_LINE+1, SIDE_LENGTH):
                                        add_move_to_solution(F"{line_BetweenCenterLineAndRight}L'")
                                    
                                    add_move_to_solution("U'")
                                    TrySolveLineUsingFrontFace()
                        else:
                            add_move_to_solution("U")
                            for line_LeftToCenterLine in range(2, CENTER_LINE):
                                add_move_to_solution(f"{line_LeftToCenterLine}L")
                            add_move_to_solution("F2")
                            for line_LeftToCenterLine in range(2, CENTER_LINE):
                                add_move_to_solution(f"{line_LeftToCenterLine}L'")
                            
                            for line_RightToCenterLine in range(CENTER_LINE+1, SIDE_LENGTH):
                                add_move_to_solution(f"{line_RightToCenterLine}L")
                            add_move_to_solution("F2")
                            for line_RightToCenterLine in range(CENTER_LINE+1, SIDE_LENGTH):
                                add_move_to_solution(f"{line_RightToCenterLine}L'")
                            add_move_to_solution("U'")
                    
                    def TrySolveLineUsingLeftAndRightFaces():
                        print("TrySolveLineUsingLeftAndRightFaces()")
                        add_move_to_solution("y")
                        add_move_to_solution("U'")

                        # "Right"
                        TrySolveLineUsingFrontFace()
                        print("[R]TrySolveLineUsingLeftAndRightFaces()")
                        # "Left"
                        if cube_nxn[TOP_FACE][piece] != colorOfStartingSide:
                            TrySolveLineUsingBackFace()

                        add_move_to_solution("U")
                        add_move_to_solution("y")
                        add_move_to_solution("y")
                        add_move_to_solution("y")
                    
                    def EjectLineBackPieces():
                        print("EjectLineBackPieces()")
                        if lineInProgress == CENTER_LINE:
                            add_move_to_solution(f"{lineInProgress}L2")
                            add_move_to_solution("F")
                            add_move_to_solution(f"{lineInProgress}L2")
                            TrySolveLineUsingFrontFace()
                        elif lineInProgress < CENTER_LINE:
                            add_move_to_solution("U")
                            add_move_to_solution(f"{line}L2")
                            add_move_to_solution("F2")
                            add_move_to_solution(f"{line}L2")
                            add_move_to_solution("U'")
                        else:
                            add_move_to_solution("U'")
                            add_move_to_solution(f"{line}L2")
                            add_move_to_solution("F2")
                            add_move_to_solution(f"{line}L2")
                            add_move_to_solution("U")
                    line = 2
                    FindMostSolvedLineOnFace(TOP_FACE, CUBE_COLORS[solvedFace], lineInProgress)

                    for piece in range((lineInProgress - 1)*SIDE_LENGTH + 1, lineInProgress*SIDE_LENGTH - 1):
                        print(f"========== {piece=} ==========")
                        if cube_nxn[TOP_FACE][piece] != colorOfStartingSide:# and piece != center:
                            # Front
                            TrySolveLineUsingFrontFace()
                        if cube_nxn[TOP_FACE][piece] != colorOfStartingSide:
                            # Top
                            TrySolveLineUsingTopFace()
                        if cube_nxn[TOP_FACE][piece] != colorOfStartingSide:
                            # Bottom
                            TrySolveLineUsingBottomFace()
                        if cube_nxn[TOP_FACE][piece] != colorOfStartingSide:
                            # Right and Left
                            TrySolveLineUsingLeftAndRightFaces()
                        if cube_nxn[TOP_FACE][piece] != colorOfStartingSide:
                            # Back
                            EjectLineBackPieces()
                        line+=1
                        continue
                        if line > CENTER_LINE:
                            inverted = True
                    line = lineInProgress
                ### line_horizontal
                def PullLine():
                    print("PullLine()")
                    if lineInProgress != CENTER_LINE:
                        result = line < CENTER_LINE
                        result = InvertResult(result) if invertPush else result
                        if result:
                            add_move_to_solution("U")
                            add_move_to_solution(f"{lineInProgress}L")
                            add_move_to_solution("U2")
                        else:
                            add_move_to_solution("U'")
                            add_move_to_solution(f"{lineInProgress}L")
                            add_move_to_solution("U2")
                        add_move_to_solution(f"{lineInProgress}L'")
                    else:
                        add_move_to_solution("U'")
                        add_move_to_solution(f"{lineInProgress}L'")
                
                PushLine()
                SolvePushedLine()
                PullLine()
            
            for line_horizontal in range(2, SIDE_LENGTH):
                invertPush = False if line_horizontal <= CENTER_LINE else True
                print(f"========== {line_horizontal=} {invertPush=} ==========")
                SolveLine(startingFace, line_horizontal, invertPush)
        def algorithm_3x3x3():
            # Ze souřadnic vrátí barvy rohu
            def get_corner_colors(corner):
                global cube_nxn
                corner=eval(corner)
                cord1=corner[0]
                cord2=corner[1]
                cord3=corner[2]
                color1=cube_nxn[cord1[0]][cord1[1]]
                color2=cube_nxn[cord2[0]][cord2[1]]
                color3=cube_nxn[cord3[0]][cord3[1]]
                a=[color1,color2,color3]
                return a
            # Ze souřadnic vrátí barvy hrany
            def get_edge_colors(edge): # Vrátit ze souřadnic barvy hrany
                global cube_nxn
                edge=eval(edge)
                cord1=edge[0]
                cord2=edge[1]
                color1=cube_nxn[cord1[0]][cord1[1]]
                color2=cube_nxn[cord2[0]][cord2[1]]
                return [color1,color2]
            # Složit kříž - hodně neefektivní (CFOP - <= 8 pohybů, tato metoda - >20 pohybů)
            def cross():
                # Převedení spodních hran nahoru
                global cube_nxn
                edge=[[5,1],[2,7]] # Výchozí bod
                for _ in range(8):
                    bottom_edge=get_edge_colors(str(edge))
                    if y in bottom_edge:
                        #do_move("3U'",show=False)
                        if bottom_edge.index(y)==0: # Pokud je žlutá dole, přesunout pomocí F2 nahoru bez narušení žlutých navrchu
                            while cube_nxn[0][7] == y or cube_nxn[2][1] == y:
                                add_move_to_solution("U")
                            add_move_to_solution("F2")
                        else: # Pokud není žlutá dole, přesunout pomocí F + R nahoru bez narušení žlutých navrchu
                            while cube_nxn[0][7] == y or cube_nxn[2][1] == y:
                                add_move_to_solution("U")
                            add_move_to_solution("F")
                            while cube_nxn[0][3] == y or cube_nxn[2][edge[0][1]] == y:
                                add_move_to_solution("U")
                            add_move_to_solution("L'")
                    add_move_to_solution("3U'")
                # Převedení hran ve střední vrstvě nahoru
                edge=[[2,5],[3,3]]
                for _ in range(4):
                    side_edge=get_edge_colors(str(edge))
                    if y in side_edge:
                        if side_edge.index(y)==0:
                            while cube_nxn[0][5] == y or cube_nxn[3][1] == y:
                                add_move_to_solution("U")
                            add_move_to_solution("3L'")
                            if y in set([cube_nxn[5][5],cube_nxn[3][7]]):
                                while cube_nxn[0][5] == y or cube_nxn[3][1] == y:
                                    add_move_to_solution("U")
                                add_move_to_solution("3L")
                        else:
                            while cube_nxn[0][7] == y or cube_nxn[2][1] == y:
                                add_move_to_solution("U")
                            add_move_to_solution("F'")
                            if y in set([cube_nxn[5][1],cube_nxn[2][7]]):
                                while cube_nxn[0][7] == y or cube_nxn[2][1] == y:
                                    add_move_to_solution("U")
                                add_move_to_solution("F")
                    add_move_to_solution("2U'")
                for _ in range(4): # Oprava otočení vrchních hran
                    top_edge=get_edge_colors(str([[0, 7], [2, 1]]))
                    if y in top_edge:
                        if top_edge.index(y)!=0:
                            add_move_to_solution("F")
                            while cube_nxn[0][5] == y or cube_nxn[3][1] == y:
                                add_move_to_solution("U'")
                            add_move_to_solution("3L'")
                        else:
                            add_move_to_solution("U'")
                for _ in range(4): # Dokončení kříže, mohlo to být napsáno v jedné funkci, ale o'well
                    if cube_nxn[2][1]==cube_nxn[2][4] and cube_nxn[0][7]==y:
                        add_move_to_solution("F2")
                        break
                    else:
                        add_move_to_solution("U'")
                for _ in range(4):
                    if cube_nxn[3][1]==cube_nxn[3][4] and cube_nxn[0][5]==y:
                        add_move_to_solution("3L2")
                        break
                    else:
                        add_move_to_solution("U'")
                for _ in range(4):
                    if cube_nxn[4][1]==cube_nxn[4][4] and cube_nxn[0][1]==y:
                        add_move_to_solution("3F2")
                        break
                    else:
                        add_move_to_solution("U'")
                for _ in range(4):
                    if cube_nxn[1][1]==cube_nxn[1][4] and cube_nxn[0][3]==y:
                        add_move_to_solution("L2")
                        break
                    else:
                        add_move_to_solution("U'")
                print("Cross solution:")
                print(algorithm_solution)
            def corners_f():
                global cube_nxn
                for corner_pos_1 in [[r,b,y],[b,o,y],[g,o,y],[g,r,y]]:
                    corner_found=False
                    if set(get_corner_colors(str([[5,2],[3,6],[2,8]])))!=set(corner_pos_1): # if corner not in the right spot
                        for _ in range(4):
                            corner_pos_2=set(get_corner_colors(str([[0,6],[1,2],[2,0]])))
                            if set(corner_pos_2)==set(corner_pos_1): # Rotate the top layer until the right corner is found
                                add_move_to_solution("3L'")
                                add_move_to_solution("U'")
                                add_move_to_solution("3L")
                                corner_found=True
                                break
                            else:
                                add_move_to_solution("U'")
                        # If the right edge is not in the top layer, search the bottom layer
                        if not corner_found:
                            for _ in range(4):
                                add_move_to_solution("3U'")
                                corner_pos_2=set(get_corner_colors(str([[5,2],[3,6],[2,8]])))
                                if set(corner_pos_2)==set(corner_pos_1): # insert, if found
                                    add_move_to_solution("3L'")
                                    add_move_to_solution("U")
                                    add_move_to_solution("3L")
                                    while cube_nxn[2][7]!=cube_nxn[2][4]:
                                        add_move_to_solution("3U")
                                    add_move_to_solution("3L'")
                                    add_move_to_solution("U'")
                                    add_move_to_solution("3L")
                                    break
                    add_move_to_solution("y")
                print("Solution for all the previous steps and inserting the corners in the right spot:")
                print(algorithm_solution)
                corner=[[5,2],[3,6],[2,8]]
                for _ in range(4): # Rotating the bottom corners
                    corner_colors = get_corner_colors(str(corner))
                    for _ in range(3):
                        if corner_colors[0]!=y: # if yellow is not on the bottom, corner is not rotated right -> rotate
                            for move in ["3L'","U","3L","U'","3L'","U","3L","U'"]:
                                add_move_to_solution(move)
                            corner_colors = get_corner_colors(str(corner))
                    add_move_to_solution("3U'")
                print("Solution for all the previous steps and rotating the corners in the bottom layer:")
                print(algorithm_solution)

            def second_layer():
                global cube_nxn
                edge=get_edge_colors(str([[2,5],[3,3]]))
                moves=[]
                for _ in range(8): # Second layer - leave solved pieces in place or take unsolved ones out
                    if cube_nxn[2][4]==edge[0] and cube_nxn[3][4]==edge[1]: # if the right edge is in the right spot, do nothing
                        pass
                    elif cube_nxn[2][4]==edge[1] and cube_nxn[3][4]==edge[0]: # if the right edge is in the right spot but flipped, flip it
                        for move in ["3L'","U","3L","U'","3L'","U","3L","U","F'","U'","F","U","F'","U'","F"]: 
                                add_move_to_solution(move)
                    else: 
                        for _ in range(4): # Rotate the top layer until the right edge is found (if present, actually)
                            if set([cube_nxn[0][3],cube_nxn[1][1]])!=set([cube_nxn[2][4],cube_nxn[3][4]]):
                                add_move_to_solution("U'")
                        if [cube_nxn[0][3],cube_nxn[1][1]]==[cube_nxn[3][4],cube_nxn[2][4]]: # Insert the right piece into the right slot the right way - 1st case
                            moves=["3L'","U","3L","U'","F'","U'","F"]
                        elif [cube_nxn[0][3],cube_nxn[1][1]]==[cube_nxn[2][4],cube_nxn[3][4]]: # Insert the right piece into the right slot the right way - 2nd case
                            moves=["U","F'","U'","F","U","3L'","U","3L"]
                        else: # Right edge not in the top
                            if w not in [cube_nxn[3][4],cube_nxn[2][4]]: # if there isn't a white edge in the right edge's slot, take it out 
                                while w not in set([cube_nxn[0][3],cube_nxn[1][1]]): # Turn the top layer until the right piece is in the top left
                                    add_move_to_solution("U'")
                                moves=["3L'","U","3L","U'","F'","U'","F"]
                        for move in moves:
                            add_move_to_solution(move)
                    add_move_to_solution("y")
                    edge=get_edge_colors(str([[2,5],[3,3]]))
                print("Solution for all the previous steps and finishing the second layer:")
                print(algorithm_solution)
            def cross_on_top():
                # making a cross on the top
                # if cross is done, stop the function
                if [cube_nxn[0][1],cube_nxn[0][3],cube_nxn[0][5],cube_nxn[0][7]]==[w,w,w,w]:
                    return
                global moves
                moves=[]
                # create the cross using a hook
                def hook():
                    global moves # Different hook cases
                    if [cube_nxn[0][1],cube_nxn[0][3]]==[w,w]:
                        moves=["F","U","3L'","U'","3L","F'"]
                        print("case4 - a hook")
                    elif [cube_nxn[0][5],cube_nxn[0][1]]==[w,w]:
                        moves=["U'","F","U","3L'","U'","3L","F'"]
                        print("case5 - a hook")
                    elif [cube_nxn[0][5],cube_nxn[0][7]]==[w,w]:
                        moves=["U2","F","U","3L'","U'","3L","F'"]
                        print("case6 - a hook")
                    elif [cube_nxn[0][7],cube_nxn[0][3]]==[w,w]:
                        moves=["U","F","U","3L'","U'","3L","F'"]
                        print("case7 - a hook")
                    for move in moves:
                        add_move_to_solution(move)
                        moves=[]
                # create the cross using a line
                if [cube_nxn[0][3],cube_nxn[0][5]]==[w,w]:
                    moves=["F","3L'","U","3L","U'","F'"]
                    print("case2 - a line")
                elif [cube_nxn[0][1],cube_nxn[0][7]]==[w,w]:
                    moves=["U","F","3L'","U","3L","U'","F'"]
                    print("case3 - a line")
                else: # There's just a dot on the top layer -> solve it into a hook, then finish
                    hook()
                    if [cube_nxn[0][1],cube_nxn[0][3],cube_nxn[0][5],cube_nxn[0][7]]!=[w,w,w,w]: # if neither a line, nor a hook are present, do a "sexy" move and then check again for a line/hook
                        for move in ["F","3L'","U","3L","U'","F'"]:
                            add_move_to_solution(move)
                            moves=[]
                        hook()
                for move in moves:
                    add_move_to_solution(move)
                print("Solution for all the previous steps and making the cross:")
                print(algorithm_solution)
            def match_side_colors():
                while cube_nxn[2][1]!=cube_nxn[2][4]:
                    add_move_to_solution("U'")
            def move_cross_on_top():
                # Putting the cross' pieces in the right spot in relation with the others
                correct_edge_order=[[cube_nxn[1][4],cube_nxn[2][4],cube_nxn[3][4],cube_nxn[4][4]],[cube_nxn[2][4],cube_nxn[3][4],cube_nxn[4][4],cube_nxn[1][4]],[cube_nxn[3][4],cube_nxn[4][4],cube_nxn[1][4],cube_nxn[2][4]],[cube_nxn[4][4],cube_nxn[1][4],cube_nxn[2][4],cube_nxn[3][4]]]
                adjacent_edges=[[cube_nxn[1][4],cube_nxn[2][4]],[cube_nxn[2][4],cube_nxn[3][4]],[cube_nxn[3][4],cube_nxn[4][4]],[cube_nxn[4][4],cube_nxn[1][4]]]
                for _ in range(4): # if the cross' pieces are located right, return
                    if [cube_nxn[1][1],cube_nxn[2][1],cube_nxn[3][1],cube_nxn[4][1]] in correct_edge_order:
                        match_side_colors()
                        return
                    for _ in range(4): # Do an algorithm in the right spot
                        if [cube_nxn[3][1],cube_nxn[4][1]] in adjacent_edges:
                            for move in ["3L'","U","3L","U","3L'","U2","3L","U"]:
                                add_move_to_solution(move)
                            match_side_colors()
                            return
                        add_move_to_solution("U'")
                    for move in ["3L'","U","3L","U","3L'","U2","3L"]:
                        add_move_to_solution(move)
                print("Solution for all the previous steps and putting the cross' pieces in the right location in relation with the other edges:")
                print(algorithm_solution)
            def move_corners():
                top_corners=[str([[0,6],[1,2],[2,0]]),str([[0,8],[2,2],[3,0]]),str([[0,0],[4,2],[1,0]]),str([[0,2],[3,2],[4,0]])]
                for _ in range(6):
                    # this corner is in the UFR slot
                    corner_base=get_corner_colors(str([[0,8],[2,2],[3,0]]))
                    # if the corner in the UFR is not equal to the edge that's supposed to be in the UFR slot
                    if y in set(corner_base): # Do nothing if the right corner is in the right spot
                        pass
                    elif set(corner_base)!=set([w,cube_nxn[2][1],cube_nxn[3][1]]): # Take out the wrong corner and rotate the bottom layer until the right corner is found, then insert it
                        add_move_to_solution("3L")
                        add_move_to_solution("3U")
                        add_move_to_solution("3L'")
                        for _ in range(4):
                            # if the UFR/URB/UBL/ULF slot is not equal to the correct slot:
                            if set([w,cube_nxn[2][1],cube_nxn[3][1]])!=set(corner_base):
                                add_move_to_solution("U'")
                        add_move_to_solution("3L")
                        add_move_to_solution("3U'")
                        add_move_to_solution("3L'")
                    add_move_to_solution("U'")
                corner_base=get_corner_colors(str([[0,8],[2,2],[3,0]]))
                if y in set(corner_base):
                    for move in ["U'","3L","3U","3L'","U","3L","3U'","3L'"]:
                        add_move_to_solution(move)
                match_side_colors()
                print("Solution for all the previous steps and moving the corners in the right spot:")
                print(algorithm_solution)
            def rotate_top_corners():
                for _ in range(4): # Rotating the corners
                    corner=get_corner_colors(str([[0,8],[2,2],[3,0]]))
                    for _ in range(3):
                        if cube_nxn[0][8]!=w: # Do a "sexy" move on the bottom until the corner is rotated right
                            for move in ["3L","3U","3L'","3U'","3L","3U","3L'","3U'"]:
                                add_move_to_solution(move)
                    add_move_to_solution("U'")
                print("Solution for all the previous steps and rotating the corners in the top layer:")
                print(algorithm_solution)
            cross()
            corners_f()
            second_layer()
            cross_on_top()
            move_cross_on_top()
            move_corners()
            rotate_top_corners()
        def simplify_solution():
            global algorithm_solution,simplified_solution
            unsimplified_length=len(algorithm_solution)
            simplified_solution=[]
            for x in range(len(algorithm_solution)): # Grouping same moves together ([["U"],["U"],["U"],["U"],["U"],["U"],["U"]] -> [["U","U","U"]])
                item1=algorithm_solution[x]
                try:
                    if item1 in simplified_solution[-1]:
                        simplified_solution[-1].append(item1)
                    else:
                        simplified_solution.append([item1])
                except:
                    simplified_solution.append([item1])
            for x in range(len(simplified_solution)): # Merging same moves (["U","U","U"] -> ["U'"])
                if len(simplified_solution[x])>=4:
                    simplified_solution[x]=simplified_solution[x][(len(simplified_solution[x])//4)*4:]
                if len(simplified_solution[x])>=2:
                    if simplified_solution[x][0] not in ["x","y","z"]:
                        if len(simplified_solution[x])==3:
                            if simplified_solution[x][0][-1]=="'":
                                simplified_solution[x]=[simplified_solution[x][0][:-1]]
                            else:
                                simplified_solution[x]=[simplified_solution[x][0]]
                        elif len(simplified_solution[x])==2:
                            simplified_solution[x]=[simplified_solution[x][0][0:2]+"2"]
            for x in range(-len(simplified_solution),0): # Final cleanup (["8F","8F'"] -> [])
                try:
                    item1=simplified_solution[x][0]
                    item2=simplified_solution[x+1][0]
                    if item1[:-1]==item2 or item1==item2[:-1]:
                        simplified_solution[x]=[]
                        simplified_solution[x+1]=[]
                except:
                    pass
            simplified_solution=sum(simplified_solution,[])
            simplified_length=len(simplified_solution)
            print(f'Difference: {unsimplified_length-simplified_length}')
            
        #algorithm_3x3x3()
        ReduceCubeAlgorithm()
        simplify_solution()
        algorithm_ended=time.time()
        #print(f'It took {round(algorithm_ended-algorithm_started,3)} seconds to solve this cube.')
        show_cube()
        print("\n\n--- Scramble ---")
        print(scramble)
        print("--- Generated Solution: ---")
        print(algorithm_solution)
        print("\n\n")
        simplify_solution()
        print("Simplified solution:")
        print(simplified_solution)
    # Funkce tlačítek
    def button_function(arg):
        global moves_done
        moves_done.append(arg)
        do_move(arg)
    # U, D pohyby
    def slice_move(slice3,slice4,shift):
        global cube_nxn
        slice_colors=[]
        for i in cube_nxn[1:5]:
            slice_colors.append(i[slice3:slice4])
        slice_colors=slice_colors[shift:]+slice_colors[:shift]
        for xa,xc in zip(range(1,5),range(len(slice_colors))):
            for xb,xd in zip(range(slice3,slice4),range(len(slice_colors[xc]))):
                cube_nxn[xa][xb] = slice_colors[xc][xd]
    # Vytvořit kostku
    def create_the_cube(show=True):
        global cube_nxn,SIDE_LENGTH,cube_nxn_solved
        cube_nxn = [[w]*SIDE_LENGTH*SIDE_LENGTH,
        [g]*SIDE_LENGTH*SIDE_LENGTH,
        [r]*SIDE_LENGTH*SIDE_LENGTH,
        [b]*SIDE_LENGTH*SIDE_LENGTH,
        [o]*SIDE_LENGTH*SIDE_LENGTH,
        [y]*SIDE_LENGTH*SIDE_LENGTH]
        cube_nxn_solved=deepcopy(cube_nxn)
        if SIDE_LENGTH == 1:
            cube_nxn[0][0] == w
        elif SIDE_LENGTH%2!=0:
            cube_nxn[0][SIDE_LENGTH**2//2]=w
        else:
            cube_nxn[0][round(SIDE_LENGTH*(SIDE_LENGTH/2)+SIDE_LENGTH/2)]=w
        if show:
            show_cube()
    # Resetovat scramble kostky
    def reset_the_cube():
        global scramble
        create_the_cube(show=False)
        for i in scramble:
            do_move(i,show=False)
        show_cube()
    # Otočení "vrchní" strany kostky
    def rotate_face(slc):
        global cube_nxn,SIDE_LENGTH
        cube_nxn[slc] = sum([list(reversed(cube_nxn[slc][i::SIDE_LENGTH])) for i in range(SIDE_LENGTH)],[])
    # Otočení strany
    def do_move(turn,show=True):
        def reverse_str(item):
            a=list(reversed(item))
            return a
        global cube_nxn,SIDE_LENGTH
        print(f'--- Move: {turn} ---')
        if turn == "y":
            cube_nxn[1],cube_nxn[2],cube_nxn[3],cube_nxn[4] = cube_nxn[2],cube_nxn[3],cube_nxn[4],cube_nxn[1]
            rotate_face(0)
            rotate_face(5)
            rotate_face(5)
            rotate_face(5)
        elif turn == "x":
            cube_nxn[0],cube_nxn[2],cube_nxn[5],cube_nxn[4] = cube_nxn[2],cube_nxn[5],cube_nxn[4],cube_nxn[0]
            rotate_face(1)
            rotate_face(1)
            rotate_face(1)
            rotate_face(3)
            rotate_face(5)
            rotate_face(5)
            rotate_face(4)
            rotate_face(4)
        elif turn == "z":
            cube_nxn[0],cube_nxn[1],cube_nxn[5],cube_nxn[3] = cube_nxn[1],cube_nxn[5],cube_nxn[3],cube_nxn[0]
            rotate_face(0)
            rotate_face(1)
            rotate_face(2)
            rotate_face(3)
            rotate_face(4)
            rotate_face(4)
            rotate_face(4)
            rotate_face(5)
        else:
            try:
                y = turn.split("U") # U a D pohyby
                if len(y) == 1:
                    raise IndexError
                try:
                    x=int(y[0])
                except:
                    x=1
                if y[1] == "":
                    slice_move((x-1)*SIDE_LENGTH,x*SIDE_LENGTH,1)
                    if x==1:
                        rotate_face(0)
                    elif x==SIDE_LENGTH:
                        rotate_face(5)
                        rotate_face(5)
                        rotate_face(5)
                if y[1] == "'":
                    slice_move((x-1)*SIDE_LENGTH,x*SIDE_LENGTH,3)
                    if x==1:
                        rotate_face(0)
                        rotate_face(0)
                        rotate_face(0)
                    elif x==SIDE_LENGTH:
                        rotate_face(5)
                elif y[1] == "2":
                    slice_move((x-1)*SIDE_LENGTH,x*SIDE_LENGTH,2)
                    if x==1:
                        rotate_face(0)
                        rotate_face(0)
                    elif x==SIDE_LENGTH:
                        rotate_face(5)
                        rotate_face(5)
            except IndexError:
                try: 
                    y = turn.split("F") # F a B pohyby
                    if len(y) == 1:
                        raise IndexError
                    try:
                        x = int(y[0])
                    except:
                        x=1
                    if y[1] == "'":
                        e=cube_nxn[3][x-1::SIDE_LENGTH]
                        f=cube_nxn[5][SIDE_LENGTH*(x-1):SIDE_LENGTH*x]
                        g=cube_nxn[1][SIDE_LENGTH-x::SIDE_LENGTH]
                        h=cube_nxn[0][SIDE_LENGTH**2-SIDE_LENGTH*x:SIDE_LENGTH**2-SIDE_LENGTH*(x-1)]
                        cube_nxn[0][SIDE_LENGTH**2-SIDE_LENGTH*x:SIDE_LENGTH**2-SIDE_LENGTH*(x-1)]=e
                        cube_nxn[3][x-1::SIDE_LENGTH]=reverse_str(f)
                        cube_nxn[5][SIDE_LENGTH*(x-1):SIDE_LENGTH*x]=g
                        cube_nxn[1][SIDE_LENGTH-x::SIDE_LENGTH]=reverse_str(h)
                        if x==1:
                            rotate_face(2)
                            rotate_face(2)
                            rotate_face(2)
                        elif x==SIDE_LENGTH:
                            rotate_face(4)	
                    elif y[1] == "":
                        e=cube_nxn[3][x-1::SIDE_LENGTH]
                        f=cube_nxn[5][SIDE_LENGTH*(x-1):SIDE_LENGTH*x]
                        g=cube_nxn[1][SIDE_LENGTH-x::SIDE_LENGTH]
                        h=cube_nxn[0][SIDE_LENGTH**2-SIDE_LENGTH*x:SIDE_LENGTH**2-SIDE_LENGTH*(x-1)]
                        cube_nxn[0][SIDE_LENGTH**2-SIDE_LENGTH*x:SIDE_LENGTH**2-SIDE_LENGTH*(x-1)]=reverse_str(g)
                        cube_nxn[3][x-1::SIDE_LENGTH]=h
                        cube_nxn[5][SIDE_LENGTH*(x-1):SIDE_LENGTH*x]=reverse_str(e)
                        cube_nxn[1][SIDE_LENGTH-x::SIDE_LENGTH]=f
                        if x==1:
                            rotate_face(2)
                        elif x==SIDE_LENGTH:
                            rotate_face(4)
                            rotate_face(4)
                            rotate_face(4)
                    else:
                        e=cube_nxn[3][x-1::SIDE_LENGTH]
                        f=cube_nxn[5][SIDE_LENGTH*(x-1):SIDE_LENGTH*x]
                        g=cube_nxn[1][SIDE_LENGTH-x::SIDE_LENGTH]
                        h=cube_nxn[0][SIDE_LENGTH**2-SIDE_LENGTH*x:SIDE_LENGTH**2-SIDE_LENGTH*(x-1)]
                        cube_nxn[0][SIDE_LENGTH**2-SIDE_LENGTH*x:SIDE_LENGTH**2-SIDE_LENGTH*(x-1)]=reverse_str(f)
                        cube_nxn[3][x-1::SIDE_LENGTH]=reverse_str(g)
                        cube_nxn[5][SIDE_LENGTH*(x-1):SIDE_LENGTH*x]=reverse_str(h)
                        cube_nxn[1][SIDE_LENGTH-x::SIDE_LENGTH]=reverse_str(e)
                        if x==1:
                            rotate_face(2)
                            rotate_face(2)
                        elif x==SIDE_LENGTH:
                            rotate_face(4)
                            rotate_face(4)
                except IndexError:
                    y = turn.split("L") # L a R pohyby
                    try:
                        x = int(y[0])
                    except:
                        x=1
                    if y[1] == "'":
                        a=cube_nxn[2][x-1::SIDE_LENGTH]
                        b=cube_nxn[5][x-1::SIDE_LENGTH]
                        c=cube_nxn[4][SIDE_LENGTH-x::SIDE_LENGTH]
                        d=cube_nxn[0][x-1::SIDE_LENGTH]
                        cube_nxn[0][x-1::SIDE_LENGTH]=a
                        cube_nxn[2][x-1::SIDE_LENGTH]=b
                        cube_nxn[5][x-1::SIDE_LENGTH]=reverse_str(c)
                        cube_nxn[4][SIDE_LENGTH-x::SIDE_LENGTH]=reverse_str(d)
                        if x==1:
                            rotate_face(1)
                            rotate_face(1)
                            rotate_face(1)
                        elif x==SIDE_LENGTH:
                            rotate_face(3)
                    elif y[1] == "":
                        a=cube_nxn[2][x-1::SIDE_LENGTH]
                        b=cube_nxn[5][x-1::SIDE_LENGTH]
                        c=cube_nxn[4][SIDE_LENGTH-x::SIDE_LENGTH]
                        d=cube_nxn[0][x-1::SIDE_LENGTH]
                        cube_nxn[0][x-1::SIDE_LENGTH]=reverse_str(c)
                        cube_nxn[2][x-1::SIDE_LENGTH]=d
                        cube_nxn[5][x-1::SIDE_LENGTH]=a
                        cube_nxn[4][SIDE_LENGTH-x::SIDE_LENGTH]=reverse_str(b)
                        if x==1:
                            rotate_face(1)
                        elif x==SIDE_LENGTH:
                            rotate_face(3)
                            rotate_face(3)
                            rotate_face(3)
                    else:
                        a=cube_nxn[2][x-1::SIDE_LENGTH]
                        b=cube_nxn[5][x-1::SIDE_LENGTH]
                        c=cube_nxn[4][SIDE_LENGTH-x::SIDE_LENGTH]
                        d=cube_nxn[0][x-1::SIDE_LENGTH]
                        cube_nxn[0][x-1::SIDE_LENGTH]=b
                        cube_nxn[2][x-1::SIDE_LENGTH]=reverse_str(c)
                        cube_nxn[5][x-1::SIDE_LENGTH]=d
                        cube_nxn[4][SIDE_LENGTH-x::SIDE_LENGTH]=reverse_str(a)
                        if x==1:
                            rotate_face(1)
                            rotate_face(1)
                        elif x==SIDE_LENGTH:
                            rotate_face(3)
                            rotate_face(3)
        if show:
            show_cube() # Zobrazení kostky
    # Ukončit
    def quit():
        global visualization,buttons_root
        visualization.destroy()
        buttons_root.destroy()
        global root
        root.destroy() # Vypnout program při kliknutí na křížek
    # Zobrazit kostku
    def show_cube():
        visualization_started=time.time()
        global logo,logo_sticker,SIDE_LENGTH
        for i in visualization.winfo_children():
            i.destroy()
        ind = 0
        for ia in range(1,SIDE_LENGTH+1):
            for ib in range(SIDE_LENGTH+1,SIDE_LENGTH*2+1):
                a = LabelFrame(visualization,bd=5)
                a.grid(row=ia,column=ib)
                b = Label(a,bg=cube_nxn[0][ind].lower(),padx=15,pady=10,bd=5)
                b.grid()
                ind+=1
        ind = 0
        for ia in range(SIDE_LENGTH+1,SIDE_LENGTH*2+1):
            for ib in range(1,SIDE_LENGTH+1):
                a = LabelFrame(visualization,bd=5)
                a.grid(row=ia,column=ib)
                b = Label(a,bg=cube_nxn[1][ind].lower(),padx=15,pady=10,bd=5)
                b.grid()
                ind+=1
        ind = 0
        for ia in range(SIDE_LENGTH*2+1,SIDE_LENGTH*3+1):
            for ib in range(SIDE_LENGTH+1,SIDE_LENGTH*2+1):
                a = LabelFrame(visualization,bd=5)
                a.grid(row=ia,column=ib)
                b = Label(a,bg=cube_nxn[5][ind].lower(),padx=15,pady=10,bd=5)
                b.grid()
                ind+=1
        ind = 0
        for ia in range(SIDE_LENGTH+1,SIDE_LENGTH*2+1):
            for ib in range(SIDE_LENGTH+1,SIDE_LENGTH*2+1):
                a = LabelFrame(visualization,bd=5)
                a.grid(row=ia,column=ib)
                b = Label(a,bg=cube_nxn[2][ind].lower(),padx=15,pady=10,bd=5)
                b.grid()
                ind+=1
        ind = 0
        for ia in range(SIDE_LENGTH+1,SIDE_LENGTH*2+1):
            for ib in range(SIDE_LENGTH*2+1,SIDE_LENGTH*3+1):
                a = LabelFrame(visualization,bd=5)
                a.grid(row=ia,column=ib)
                b = Label(a,bg=cube_nxn[3][ind].lower(),padx=15,pady=10,bd=5)
                b.grid()
                ind+=1
        ind = 0
        for ia in range(SIDE_LENGTH+1,SIDE_LENGTH*2+1):
            for ib in range(SIDE_LENGTH*3+1,SIDE_LENGTH*4+1):
                a = LabelFrame(visualization,bd=5)
                a.grid(row=ia,column=ib)
                b = Label(a,bg=cube_nxn[4][ind].lower(),padx=15,pady=10,bd=5)
                b.grid()
                ind+=1 # Zobrazit kostku
        visualization_finished=time.time()
        print(f'Cube visualization took {round(visualization_finished-visualization_started,3)} seconds.')
    # Undo tlačítko
    def undo(move):
        global moves_done,undone_moves
        try:
            last_move=moves_done[-1]
            do_move(last_move)
            do_move(last_move)
            do_move(last_move)
            del moves_done[-1]
            undone_moves.append(last_move)
        except:pass
    # Redo tlačítko
    def redo(move):
        global moves_done,undone_moves
        try:
            last_move=undone_moves[-1]
            do_move(last_move)
            del undone_moves[-1]
            moves_done.append(last_move)
        except:pass# Tlačítka - redo
    # Náhodné zamíchání
    def rndsc():
        scramble_gen_start=time.time()
        global turns,scramble
        rndsc_turns=deepcopy(turns)
        rndsc_turns.remove("x")
        rndsc_turns.remove("y")
        rndsc_turns.remove("z")
        scramble=[]
        scramble.append(random.choice(rndsc_turns))
        for i in range(SIDE_LENGTH**2):
            while True:
                turn = random.choice(rndsc_turns)
                if turn[0] != scramble[-1][0]:
                    scramble.append(turn)
                    break
        scramble_gen_end=time.time()
        print(f'Generating a scramble took {round(scramble_gen_end-scramble_gen_start,3)} seconds.')
        applying_moves_start=time.time()
        create_the_cube(show=0)
        for i in scramble:
            do_move(i,show=0)
        applying_moves_end=time.time()
        print(f'Applying the scramble took {round(applying_moves_end-applying_moves_start,3)} seconds.')
        show_cube()# Tlačítka - zamíchání kostky
        program_title(scramble)
    def debug_moves():
        help_moves = ['y', 'y', 'x', 'x', '2L', 'U2', "2L'", 'U', 'U', 'U', 'U', 'U', 'U', 'F', 'F', 'F', "3L'", "U'", '3L', 'U', 'F', 'F', 'F', 'F', "U'", '4L', 'F2', "4L'", 'U', 'F', 'F', 'F', 'F', '5U', '5U', '5U', '4L2', "U'", '4L2', 'U', 'U', '2L', 'U2', "2L'"]



        for move in help_moves:	
            do_move(move,show=False)
        show_cube()
    # Panel tlačítek
    def buttons_gui(): 
        global buttons_root,SIDE_LENGTH,mod_scramble
        turns_buttons=deepcopy(turns) # Srovnání délky tlačítek
        max_len=len(str(max(turns_buttons,key=len)))
        buttons_root = Toplevel() # Config tlačítkového panelu
        buttons_root.title("These Moves Can Be Applied:")
        buttons_root.protocol("WM_DELETE_WINDOW",quit)
        buttons = LabelFrame(buttons_root,bd=10)
        buttons.grid()
        ind = 0
        rw = 1
        for txt,i in zip(turns_buttons,turns): # Zobrazení tlačítek
            if txt in reverse_translation: # Převod (např. 4L na R') - tlačítko má jiný parametr funkce než je jeho text
                txt=reverse_translation[txt]
            txt=txt+" "*(max_len-len(txt))
            #print(f'Button function: {i} | Button text: {txt}')
            btn = Button(buttons,text=txt,command=lambda var=i: button_function(var))
            btn.grid(row=rw,column=ind)
            ind+=1 # Logika zobrazení
            if ind == 20:
                ind = 0
                rw+=1

        reset_the_cube_button = Button(buttons,text="Scra.",command=reset_the_cube).grid(row=rw+1,column=0,columnspan=2) # Zobrazení misc tlačítek
        solve_the_cube_button = Button(buttons,text="Reset",command=create_the_cube).grid(row=rw+1,column=2,columnspan=2)
        undo_button = Button(buttons,text="Undo ",command=lambda var=txt: undo(var)).grid(row=rw+1,column=4,columnspan=2)
        redo_button = Button(buttons,text="Redo ",command=lambda var=txt: redo(var)).grid(row=rw+1,column=6,columnspan=2)
        random_scramble_button = Button(buttons,text="RNDSC",command=rndsc).grid(row=rw+1,column=8,columnspan=2)
        solve_button = Button(buttons,text="Solve",command=find_a_solution).grid(row=rw+1,column=10,columnspan=2)
        quit_button = Button(buttons,text="Quit ",command=quit).grid(row=rw+1,column=14,columnspan=2)
        debug_button = Button(buttons,text="Debug",command=debug_moves).grid(row=rw+1,column=12,columnspan=2)
    # Nastaví scramble jako nadpis programu
    def program_title(scramble):
        global visualization
        scramble_title=[] # V 4x4 v kódu je pohyb R označován jako 4L' - převod 4L' -> R
        for x in range(len(scramble)):
            if scramble[x] in reverse_translation:
                scramble_title.append(reverse_translation[scramble[x]])
            else:
                scramble_title.append(scramble[x])
        visualization.title(" ".join(scramble_title))
    visualization = Toplevel()
    #visualization.iconbitmap("rubiks_cube_icon.ico")
    visualization.protocol("WM_DELETE_WINDOW",quit)
    create_the_cube(show=False)
    buttons_gui()
    program_title(scramble)
    applying_moves_start=time.time()
    for i in scramble:	
        do_move(i,show=0)
        
    applying_moves_end=time.time()
    print(f'Applying the scramble took {round(applying_moves_end-applying_moves_start,3)} seconds.')
    show_cube()
    find_a_solution()
def show_scramble():
    global scramble,session,SIDE_LENGTH,frame,turns
    SIDE_LENGTH = int(session.split("x")[0])
    scramble = []
    turns = ["L","L'","L2","U","U'","U2","F","F'","F2"]
    turns_ = []
    for ia in range(SIDE_LENGTH-2):
        for ib in turns:
            turns_.append(f"{ia+2}{ib}")
    turns.extend(turns_)
    turns_=deepcopy(turns)
    for i in ["L'","L","L2","U'","U","U2","F'","F","F2"]:
        turns.insert(9,str(SIDE_LENGTH)+i)
    scramble.append(random.choice(turns))
    for i in range(0,random.randint(SIDE_LENGTH*10-SIDE_LENGTH,SIDE_LENGTH*10)):
        while True:
            temp = random.choice(turns)
            if temp[0] != scramble[-1][0]:
                scramble.append(temp)
                break
    turns.extend(["x","y","z"])
    #visualize(["2L'", 'F', '3L', 'U2', '5U2', '2U2', '3F', '5U', '3L2', 'L2', '3L', '2U', '3U', '2U', '5L', 'L', "5F'", "2U'", 'L2', '4U', "L'", '5U', "4F'", "5F'", "L'", '2U2', "5U'", '3U', '4L2', 'L', 'F2', '5F', "U'", "3L'", "4U'", '5L2', "L'", '3L2', '4U2', '5U2', '3L2', '5U', "3U'", '2U2', "L'", '4U2', "3F'"],turns)
    visualize(["2L'", "5U'", "3F'", '5U2', '2U', "5U'", '3F', "4U'", '2F2', '3U2', '2L', "3F'", '5F2', 'F', '4U2', 'L2', '3U2', "2L'", '4F2', "2F'", '5L2', '2U2', "3F'", '4U2', "2U'", '5L2'], turns)


show_scramble()
root.mainloop()