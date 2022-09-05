import random,time,os,webbrowser
from unittest import addModuleCleanup
from tkinter import *
from tkinter.filedialog import askopenfile,askdirectory
from tkinter import messagebox
from class_TextScroll import TextScroll
from class_DropDownMenu import DropDownMenu	
from PIL import ImageTk,Image
from copy import deepcopy
#from class_ScrollWindow import ScrollWindow_Extract,DropDownMenu_extract,ScrollWindow
root = Tk()
root.title("Ignac's Timer")
root.iconbitmap("rubiks_cube_icon.ico")
frame = LabelFrame(root,bd=5,width=800,height=171)
frame.grid(row=2,column=2,columnspan=4)
frame.grid_propagate(False)
top = LabelFrame(root,bd=5)
top.grid(row=1,columnspan=4,sticky=W)
left = LabelFrame(root,bd=5,width=118,height=177)
left.grid(row=2,column=1)
left.grid_propagate(False)
bottom = LabelFrame(root,bd=5)
bottom.grid(row=3,column=3,sticky=W)
bottom_buttons = LabelFrame(root,bd=5)
bottom_buttons.grid(row=3,column=2,sticky=W)
status = Label(bottom,text="Best: 0 | Worst: 0 | Ao5: 0 | Ao12: 0 | Ao50: 0 | Ao100: 0")
status.grid()
corner = LabelFrame(root,bd=5)
corner.grid(row=3,column=1)
inspection_time_default = 15
timer_accuracy = 1
open_windows = [False,False,False,False]
show_cube_bool = 1
session="5x5"
logo_sticker = "YJ.jpg"
suppressed = False
events = {'2x2': [], '3x3': [], '4x4': [], '5x5': [], '6x6': [], '7x7': [], 'Skewb': [], 'Megaminx': [], 'Pyraminx': [], 'Clock': [], 'Square One': []}

#root.state("zoomed")
def visualize(input_scramble,available_turns):
	global cube_nxn,side_length,visualization,buttons_root,moves_done,undone_moves,root,cube_nxn_solved,scramble,temp_debug_moves,temp_debug_move_index
	turns = available_turns
	temp_debug_moves = []
	temp_debug_move_index=0
	# scramble is a global variable in this function - this might change the main program's scramble!!!
	scramble = input_scramble
	scramble = ['4F2', "3L'", 'U2', '3L', '5F2', '4F2', '5L', "4F'", "3U'", 'L2', '4U', "U'", "4U'", "F'", '2U2', "L'", '3F2', '4L', "U'", '3U', '2U', '5L', "2L'", '4F2', '5U2', "3U'", '2U2', '4U2', '5F', '4L2', "5F'", "2U'", 'U2', '4L', "3U'", '2L', '3L2', '5L', 'U2', "5U'", "3U'", '4F2', '2U2', 'L2', "F'", '2F2', 'L2', 'F']
	reverse_translation={str(side_length)+"L'": 'R', str(side_length)+'L': "R'", str(side_length)+'L2': 'R2', str(side_length)+"U'": 'D', str(side_length)+'U': "D'", str(side_length)+'U2': 'D2', str(side_length)+"F'": 'B', str(side_length)+'F': "B'", str(side_length)+'F2': 'B2'}
	moves_done=[]
	undone_moves=[]
	o = "Orange"
	r = "Red"
	g = "Green"
	b = "Blue"
	y = "Yellow"
	w = "White"
	c = "Cyan"
	# Algoritmus na složení 3x3
	def find_a_solution():
		print(f"\n\n\n\n\nAlgorithm Start\nScramble: {scramble}\n\n\n\n\n")
		algorithm_started=time.time()
		global cube_nxn,cube_nxn_solved,algorithm_solution,simplified_solution,temp_debug_moves
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
		center=round((side_length**2)/2)
		while cube_nxn[0][center]!=c and cube_nxn[2][center]!=c and cube_nxn[5][center]!=c:
			add_move_to_solution("y")
		while cube_nxn[0][center]!=c:
			add_move_to_solution("x")
		while cube_nxn[2][center]!=r:
			add_move_to_solution("y")
		def algorithm_n_x_n():
			# AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH, je to příšerný kód, ale docela to funguje. 16/8/2021 23:37 - úspěšnost tak 40% | 17.8.2021 19:30 - úspěšnost 100% | 30.8.2021 - až teď úspěšnost 100% na NxN
			print("------------- NxNxN algorithm --------------")
			# Solving each horizontal line
			for color in [b,g]:
				print(f"---------- SOLVING THE {color.upper()} SIDE ------------")
				#for line,line_total in zip(sum([list(range(1,side_length//2+1)),list(range(1,side_length//2))],[]),sum([list(range(1,side_length//2+1)),list(range(1,side_length//2))],[])):
				for line,line_total in zip(sum([list(range(1,side_length//2+1)),list(reversed(range(1,side_length//2)))],[]),range(1,side_length-1)):
					#print(f'\n\n----------------------------------------------------------------------- line: {line} -----------------------------------------------------------\n\n')
					add_move_to_solution(f"{side_length-line_total}F'")
					line_solved=True
					for piece in range(side_length*line_total+1,side_length*line_total+side_length-1):
						if cube_nxn[0][piece]!=color:
							line_solved=False
							break
					add_move_to_solution(f"{side_length-line_total}F")
					if not line_solved:
						pieces_in_line={1:[],2:[],3:[],4:[]}
						# Check all lines and find the one with the most pieces solved, then rotate to it
						for rotation in range(1,5):
							for piece in range(side_length*line+1,side_length*line+side_length-1):
								#print(f'piece: {piece}')
								pieces_in_line[rotation].append(cube_nxn[0][piece])
							add_move_to_solution("U'")
							pieces_in_line[rotation]=pieces_in_line[rotation].count(color)
						pieces_in_line_values = list(pieces_in_line.values())
						for i in range(pieces_in_line_values.index(max(pieces_in_line_values))): # Put the line that has the most solved pieces on top
							add_move_to_solution("U'")
						# Solve a line
						#print("Solving a line")
						for piece in range(side_length*line+1,side_length*line+side_length-1):
							#print(f'------------ piece: {piece} -----------------------')
							if piece!=round((side_length**2)/2):
								if cube_nxn[0][piece]!=color:
									# Right piece not in the top layer, trying other layers
									#print("B) trying to find pieces in the F layer")
									for _ in range(4): # F layer
										if cube_nxn[2][piece]==color:
											layer=piece-(piece//side_length)*side_length+1
											add_move_to_solution(f"{layer}L'")
											break
										add_move_to_solution("F")
								
								if cube_nxn[0][piece]!=color:
									#print("C) trying to find pieces in the D layer")
									for _ in range(4): # D layer
										if cube_nxn[5][piece]==color:
											layer=piece-(piece//side_length)*side_length+1
											add_move_to_solution(f"{layer}L2")
											break
										add_move_to_solution(f"{side_length}U'")
								if cube_nxn[0][piece]!=color:
									#print("D) trying to find pieces in the B layer")
									for _ in range(4): # B layer
										if cube_nxn[4][piece]==color:
											layer=piece-(piece//side_length)*side_length+1
											add_move_to_solution(f"{side_length}F2")
											add_move_to_solution(f"{layer}L")
											break
										add_move_to_solution(f"{side_length}F")
								if cube_nxn[0][piece]!=color:
									#print("E) trying to find pieces in the L layer")
									for _ in range(4): # L layer
										if cube_nxn[1][piece]==color:
											layer=piece-(piece//side_length)*side_length+1
											add_move_to_solution("y")
											add_move_to_solution("y")
											add_move_to_solution("y")
											add_move_to_solution("U")
											add_move_to_solution(f"{layer}L'")
											if layer<side_length/2:
												add_move_to_solution("U")
												add_move_to_solution(f"{layer}L")
												add_move_to_solution("U2")
												add_move_to_solution("y")
											else:
												add_move_to_solution("U'")
												add_move_to_solution(f"{layer}L")
												add_move_to_solution("y")
											break
										add_move_to_solution("L")
								if cube_nxn[0][piece]!=color:
									#print("F) trying to find pieces in the R layer")
									add_move_to_solution(f"{side_length}L'")
									for i in range(2,side_length):
										if piece in list(range(side_length*(i-1)+1,side_length*(i-1)+side_length-1)):
											#print(f"piece: {piece} | i: {i}")
											add_move_to_solution(f"{i}U")
											layer_completion=[]

											for layer_piece in range(side_length*line+1,side_length*line+side_length-1):
												layer_completion.append(cube_nxn[2][layer_piece])
											if list(set(layer_completion))!=[color]:
												if i!=side_length//2+1:
													add_move_to_solution("F2")
													add_move_to_solution(f"{i}U'")
													add_move_to_solution("F2")
												else:
													add_move_to_solution("F")
													add_move_to_solution(f"{i}U'")
													add_move_to_solution("F'")
												break
											else:
												add_move_to_solution(f"{i}U'")
										#else:
										#print(f"piece ({piece}) not in range ({i})")
									add_move_to_solution(f"{side_length}L")
									if cube_nxn[0][piece]!=color:
										for _ in range(4): # F layer
											if cube_nxn[2][piece]==color:
												layer=piece-(piece//side_length)*side_length+1
												add_move_to_solution(f"{layer}L'")
												break
											add_move_to_solution("F")
								if cube_nxn[0][piece]!=color:
									#print("A) trying to find pieces in the U layer")
									add_move_to_solution("U'")
									for i in range(line+2,side_length):
										add_move_to_solution(f"{i}L")
									for i in range(2,line+1):
										add_move_to_solution(f"{i}L")
									add_move_to_solution("U")
									for _ in range(4): # F layer
										if cube_nxn[2][piece]==color:
											layer=piece-(piece//side_length)*side_length+1
											add_move_to_solution(f"{layer}L'")
											break
										add_move_to_solution("F")
							#else:
							#print("centers do not need to be solved")
						#for layer_piece in range(side_length*line+1,side_length*line+side_length-1):
						#	print(cube_nxn[0][layer_piece])
						#	if cube_nxn[0][layer_piece]!=color:
						#		print("--- ERROR ---")
						if line==side_length//2:
							#print("middle layer insert")
							add_move_to_solution("U")
							add_move_to_solution(f"{side_length-line}F'")
							add_move_to_solution("U'")
							add_move_to_solution(f"{side_length-line}F")
						else:
							#print("normal insert")
							add_move_to_solution(f"{side_length-line}F")
							add_move_to_solution(f"{side_length}L2")
							add_move_to_solution(f"{side_length-line}F'")
							add_move_to_solution(f"{side_length}L2")
						
					#else:
					#	print("skipping this line")
					#print(algorithm_solution)
				add_move_to_solution("y")
				add_move_to_solution("y")

			print(algorithm_solution)
			print("\n\n\n Solving the orange center!\n\n\n")
			while cube_nxn[4][(side_length**2)//2]!=o:
				add_move_to_solution(f"{side_length//2+1}L")
			color=o
			line_solved = False
			def solveThirdFace() -> None:
				for line in range(1, side_length - 1):
					for piece in range(side_length*line+1,side_length*(line+1)-2):
						if cube_nxn[4][piece] == o:
							line_solved = True
						elif piece == side_length**2//2:
							pass
						else:
							print("not orange piece detected")
							line_solved = False
							add_move_to_solution(f"{side_length-line}L")
							break
					if not line_solved:
						pieces_in_line={1:[],2:[],3:[],4:[]}
						# Check all lines and find the one with the most pieces solved, then rotate to it
						for rotation in range(1,5):
							for piece in range(side_length*line+1,side_length*line+side_length-1):
								pieces_in_line[rotation].append(cube_nxn[0][piece])
							add_move_to_solution("U'")
							pieces_in_line[rotation]=pieces_in_line[rotation].count(o)
						print(F"{pieces_in_line=}")
						pieces_in_line_values = list(pieces_in_line.values())
						for _ in range(pieces_in_line_values.index(max(pieces_in_line_values))): # Put the line that has the most solved pieces on top
							add_move_to_solution("U'")
						for top_piece in range(side_length*line+1,side_length*line+side_length-1):
							if cube_nxn[0][top_piece] != o:
								# Front face
								for _ in range(side_length-2):
									if cube_nxn[2][top_piece] == o:
										add_move_to_solution(f"{line+1}L'")
									else:
										add_move_to_solution("F")
								# Bottom Face
								# Top Face
								# Back Face
						break
				[print(move) for move in temp_debug_moves]
			solveThirdFace()
			"""
			for line,line_total in zip(sum([list(range(1,side_length//2+1)),list(reversed(range(1,side_length//2)))],[]),range(1,side_length-1)):
				
				print(f'\n\n-------------------- line: {line} --------------------------------------------------------------------------------------------\n\n')
				line_solved=True
				add_move_to_solution(f"{line_total+1}L")
				add_move_to_solution("U")
				for piece in range(side_length*line_total+1,side_length*line_total+side_length-1):
					print(f"piece: {piece} | color: {cube_nxn[0][piece]}")
					if cube_nxn[0][piece]!=color:
						line_solved=False
						#break
				add_move_to_solution("U'")
				add_move_to_solution(f"{line_total+1}L'")
				if not line_solved:
					pieces_in_line={1:[],2:[],3:[],4:[]}
					# Check all lines and find the one with the most pieces solved, then rotate to it
					for rotation in range(1,5):
						for piece in range(side_length*line_total+1,side_length*line_total+side_length-1):
							#print(f'piece: {piece}')
							pieces_in_line[rotation].append(cube_nxn[0][piece])
						add_move_to_solution("U'")
						pieces_in_line[rotation]=pieces_in_line[rotation].count(color)
						print(pieces_in_line)
					for i in range(list(pieces_in_line.values()).index(max(list(pieces_in_line.values())))): # Put the line that has the most solved pieces on top
						add_move_to_solution("U'")
					for piece in range(side_length*line_total+1,side_length*line_total+side_length-1):
						print(f"--------------- piece: {piece} ---------------")
						if piece!=(side_length**2)//2:
							layer=piece-(piece//side_length)*side_length+1
							if cube_nxn[0][piece]!=color:
								# Right piece not in the top layer, trying other layers
								print("A) trying to find pieces in the F layer")
								for _ in range(4): # F layer
									if cube_nxn[2][piece]==color:
										#layer=piece-(piece//side_length)*side_length+1
										add_move_to_solution(f"{layer}L'")
										if line_total+layer not in range(side_length-1,side_length+2):
											add_move_to_solution("U")
											add_move_to_solution(f"{layer}L")
											add_move_to_solution("U'")
										else:
											add_move_to_solution("U'")
											add_move_to_solution(f"{layer}L")
											add_move_to_solution("U")
										break
									add_move_to_solution("F")
							if cube_nxn[0][piece]!=color:
								print("B) trying to find pieces in the D layer")
								for _ in range(4): # D layer
									if cube_nxn[5][piece]==color:
										#       40 - (40//7)*7+1=40-5*7+1=40-35+1=4
										#layer=piece-(piece//side_length)*side_length+1
										add_move_to_solution(f"{layer}L2")
										#     5      <   4
										#if layer<=side_length//2:
										if line_total+layer not in range(side_length-1,side_length+2):
											add_move_to_solution("U")
											add_move_to_solution(f"{layer}L2")
											add_move_to_solution("U'")
										else:
											add_move_to_solution("U'")
											add_move_to_solution(f"{layer}L2")
											add_move_to_solution("U")
										break
									add_move_to_solution(f"{side_length}U'")
							
							if cube_nxn[0][piece]!=color:
								print("C) trying to find pieces in the U layer")
								layer=piece-(piece//side_length)*side_length+1
								if line_total+layer not in range(side_length-1,side_length+2):
										add_move_to_solution("U")
										add_move_to_solution(f"{layer}L2")
										add_move_to_solution("U'")
									else:
										add_move_to_solution("U'")
										add_move_to_solution(f"{layer}L2")
										add_move_to_solution("U")
									break
							
							()
							()
					if line==side_length//2:
						print("--- middle layer insert ---")
						add_move_to_solution(f"{side_length//2+1}L")
						add_move_to_solution("U'")
						add_move_to_solution(f"{side_length//2+1}L'")
					else:
						print("--- normal insert ---")
						if line_total+layer not in range(side_length-1,side_length+2):
							add_move_to_solution("U")
							add_move_to_solution(f"{line_total+1}L")
							add_move_to_solution("U2")
							add_move_to_solution(f"{line_total+1}L'")
						else:
							add_move_to_solution("U'")
							add_move_to_solution(f"{line_total+1}L'")
							add_move_to_solution(f"{side_length}F2")
							add_move_to_solution(f"{line_total+1}L")
							add_move_to_solution(f"{side_length}F2")
					print(algorithm_solution)

			"""
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
		if session=="3x3":
			algorithm_3x3x3()
		else:
			algorithm_n_x_n()
			# Convert an NXN into a 3x3
			# algorithm_3x3x3()
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
		global cube_nxn,side_length,cube_nxn_solved
		cube_nxn = [[w]*side_length*side_length,
		[g]*side_length*side_length,
		[r]*side_length*side_length,
		[b]*side_length*side_length,
		[o]*side_length*side_length,
		[y]*side_length*side_length]
		cube_nxn_solved=deepcopy(cube_nxn)
		if side_length == 1:
			cube_nxn[0][0] = c
		elif side_length%2!=0:
			cube_nxn[0][side_length**2//2]=c
		else:
			cube_nxn[0][round(side_length*(side_length/2)+side_length/2)]=c
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
		global cube_nxn,side_length
		cube_nxn[slc] = sum([list(reversed(cube_nxn[slc][i::side_length])) for i in range(side_length)],[])
	# Otočení strany
	def do_move(turn,show=True):
		def reverse_str(item):
			a=list(reversed(item))
			return a
		global cube_nxn,side_length
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
					slice_move((x-1)*side_length,x*side_length,1)
					if x==1:
						rotate_face(0)
					elif x==side_length:
						rotate_face(5)
						rotate_face(5)
						rotate_face(5)
				if y[1] == "'":
					slice_move((x-1)*side_length,x*side_length,3)
					if x==1:
						rotate_face(0)
						rotate_face(0)
						rotate_face(0)
					elif x==side_length:
						rotate_face(5)
				elif y[1] == "2":
					slice_move((x-1)*side_length,x*side_length,2)
					if x==1:
						rotate_face(0)
						rotate_face(0)
					elif x==side_length:
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
						e=cube_nxn[3][x-1::side_length]
						f=cube_nxn[5][side_length*(x-1):side_length*x]
						g=cube_nxn[1][side_length-x::side_length]
						h=cube_nxn[0][side_length**2-side_length*x:side_length**2-side_length*(x-1)]
						cube_nxn[0][side_length**2-side_length*x:side_length**2-side_length*(x-1)]=e
						cube_nxn[3][x-1::side_length]=reverse_str(f)
						cube_nxn[5][side_length*(x-1):side_length*x]=g
						cube_nxn[1][side_length-x::side_length]=reverse_str(h)
						if x==1:
							rotate_face(2)
							rotate_face(2)
							rotate_face(2)
						elif x==side_length:
							rotate_face(4)	
					elif y[1] == "":
						e=cube_nxn[3][x-1::side_length]
						f=cube_nxn[5][side_length*(x-1):side_length*x]
						g=cube_nxn[1][side_length-x::side_length]
						h=cube_nxn[0][side_length**2-side_length*x:side_length**2-side_length*(x-1)]
						cube_nxn[0][side_length**2-side_length*x:side_length**2-side_length*(x-1)]=reverse_str(g)
						cube_nxn[3][x-1::side_length]=h
						cube_nxn[5][side_length*(x-1):side_length*x]=reverse_str(e)
						cube_nxn[1][side_length-x::side_length]=f
						if x==1:
							rotate_face(2)
						elif x==side_length:
							rotate_face(4)
							rotate_face(4)
							rotate_face(4)
					else:
						e=cube_nxn[3][x-1::side_length]
						f=cube_nxn[5][side_length*(x-1):side_length*x]
						g=cube_nxn[1][side_length-x::side_length]
						h=cube_nxn[0][side_length**2-side_length*x:side_length**2-side_length*(x-1)]
						cube_nxn[0][side_length**2-side_length*x:side_length**2-side_length*(x-1)]=reverse_str(f)
						cube_nxn[3][x-1::side_length]=reverse_str(g)
						cube_nxn[5][side_length*(x-1):side_length*x]=reverse_str(h)
						cube_nxn[1][side_length-x::side_length]=reverse_str(e)
						if x==1:
							rotate_face(2)
							rotate_face(2)
						elif x==side_length:
							rotate_face(4)
							rotate_face(4)
				except IndexError:
					y = turn.split("L") # L a R pohyby
					try:
						x = int(y[0])
					except:
						x=1
					if y[1] == "'":
						a=cube_nxn[2][x-1::side_length]
						b=cube_nxn[5][x-1::side_length]
						c=cube_nxn[4][side_length-x::side_length]
						d=cube_nxn[0][x-1::side_length]
						cube_nxn[0][x-1::side_length]=a
						cube_nxn[2][x-1::side_length]=b
						cube_nxn[5][x-1::side_length]=reverse_str(c)
						cube_nxn[4][side_length-x::side_length]=reverse_str(d)
						if x==1:
							rotate_face(1)
							rotate_face(1)
							rotate_face(1)
						elif x==side_length:
							rotate_face(3)
					elif y[1] == "":
						a=cube_nxn[2][x-1::side_length]
						b=cube_nxn[5][x-1::side_length]
						c=cube_nxn[4][side_length-x::side_length]
						d=cube_nxn[0][x-1::side_length]
						cube_nxn[0][x-1::side_length]=reverse_str(c)
						cube_nxn[2][x-1::side_length]=d
						cube_nxn[5][x-1::side_length]=a
						cube_nxn[4][side_length-x::side_length]=reverse_str(b)
						if x==1:
							rotate_face(1)
						elif x==side_length:
							rotate_face(3)
							rotate_face(3)
							rotate_face(3)
					else:
						a=cube_nxn[2][x-1::side_length]
						b=cube_nxn[5][x-1::side_length]
						c=cube_nxn[4][side_length-x::side_length]
						d=cube_nxn[0][x-1::side_length]
						cube_nxn[0][x-1::side_length]=b
						cube_nxn[2][x-1::side_length]=reverse_str(c)
						cube_nxn[5][x-1::side_length]=d
						cube_nxn[4][side_length-x::side_length]=reverse_str(a)
						if x==1:
							rotate_face(1)
							rotate_face(1)
						elif x==side_length:
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
		global logo,logo_sticker,side_length
		from PIL import ImageTk,Image
		logo = ImageTk.PhotoImage(Image.open(logo_sticker).resize((30, 35), Image.ANTIALIAS))
		for i in visualization.winfo_children():
			i.destroy()
		ind = 0
		for ia in range(1,side_length+1):
			for ib in range(side_length+1,side_length*2+1):
				a = LabelFrame(visualization,bd=5)
				a.grid(row=ia,column=ib)
				if cube_nxn[0][ind] == "Cyan":
					b = Label(a,image=logo,padx=15,pady=10,bd=5)
				else:
					b = Label(a,bg=cube_nxn[0][ind].lower(),padx=15,pady=10,bd=5)
				b.grid()
				ind+=1
		ind = 0
		for ia in range(side_length+1,side_length*2+1):
			for ib in range(1,side_length+1):
				a = LabelFrame(visualization,bd=5)
				a.grid(row=ia,column=ib)
				if cube_nxn[1][ind] == "Cyan":
					b = Label(a,image=logo,padx=15,pady=10,bd=5)
				else:
					b = Label(a,bg=cube_nxn[1][ind].lower(),padx=15,pady=10,bd=5)
				b.grid()
				ind+=1
		ind = 0
		for ia in range(side_length*2+1,side_length*3+1):
			for ib in range(side_length+1,side_length*2+1):
				a = LabelFrame(visualization,bd=5)
				a.grid(row=ia,column=ib)
				if cube_nxn[5][ind] == "Cyan":
					b = Label(a,image=logo,padx=15,pady=10,bd=5)
				else:
					b = Label(a,bg=cube_nxn[5][ind].lower(),padx=15,pady=10,bd=5)
				b.grid()
				ind+=1
		ind = 0
		for ia in range(side_length+1,side_length*2+1):
			for ib in range(side_length+1,side_length*2+1):
				a = LabelFrame(visualization,bd=5)
				a.grid(row=ia,column=ib)
				if cube_nxn[2][ind] == "Cyan":
					b = Label(a,image=logo,padx=15,pady=10,bd=5)
				else:
					b = Label(a,bg=cube_nxn[2][ind].lower(),padx=15,pady=10,bd=5)
				b.grid()
				ind+=1
		ind = 0
		for ia in range(side_length+1,side_length*2+1):
			for ib in range(side_length*2+1,side_length*3+1):
				a = LabelFrame(visualization,bd=5)
				a.grid(row=ia,column=ib)
				if cube_nxn[3][ind] == "Cyan":
					b = Label(a,image=logo,padx=15,pady=10,bd=5)
				else:
					b = Label(a,bg=cube_nxn[3][ind].lower(),padx=15,pady=10,bd=5)
				b.grid()
				ind+=1
		ind = 0
		for ia in range(side_length+1,side_length*2+1):
			for ib in range(side_length*3+1,side_length*4+1):
				a = LabelFrame(visualization,bd=5)
				a.grid(row=ia,column=ib)
				if cube_nxn[4][ind] == "Cyan":
					b = Label(a,image=logo,padx=15,pady=10,bd=5)
				else:
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
		for i in range(side_length**2):
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
		global temp_debug_moves,temp_debug_move_index
		#for move in temp_debug_moves:	
		do_move(temp_debug_moves[temp_debug_move_index],show=False)	
		temp_debug_move_index+=1
		temp_debug_move_index %= len(temp_debug_moves)
		show_cube()
	# Panel tlačítek
	def buttons_gui(): 
		global buttons_root,side_length,mod_scramble
		turns_buttons=deepcopy(turns) # Srovnání délky tlačítek
		max_len=len(str(max(turns_buttons,key=len)))
		buttons_root = Toplevel() # Config tlačítkového panelu
		buttons_root.title("These Moves Can Be Applied:")
		buttons_root.iconbitmap("rubiks_cube_icon.ico")
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
	visualization.iconbitmap("rubiks_cube_icon.ico")
	visualization.protocol("WM_DELETE_WINDOW",quit)
	"""
	scrolly = Scrollbar(visualization,orient=VERTICAL)
	scrolly.grid(row=20, column=20, sticky="ns")
	scrolly.config(yscrollcommand=visualization.yview)
	"""
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
def suppress():
	global suppressed
	if not suppressed and messagebox.askyesno("Cube Could Not Be Displayed",f"Parameter 'side_length' must be a positive integer smaller than 50 (performance reasons), not {side_length}. Click on 'Yes' to suppress this warning.",icon='warning'):
		suppressed = True
def show_scramble():
		global frame,show_cube_bool,scramble,session,side_length,frame,turns
		try:
			if int(session.split("x")[0]) < 1 or type(int(session.split("x")[0])) == float or int(session.split("x")[0]) >= 50:
				raise ValueError
		except ValueError:
			if show_cube_bool:
				suppress()
			return
		side_length = int(session.split("x")[0])
		scramble = []
		turns = ["L","L'","L2","U","U'","U2","F","F'","F2"]
		turns_ = []
		for ia in range(side_length-2):
			for ib in turns:
				turns_.append(f"{ia+2}{ib}")
		turns.extend(turns_)
		turns_=deepcopy(turns)
		for i in ["L'","L","L2","U'","U","U2","F'","F","F2"]:
			turns.insert(9,str(side_length)+i)
		scramble.append(random.choice(turns))
		for i in range(0,random.randint(side_length*10-side_length,side_length*10)):
			while True:
				temp = random.choice(turns)
				if temp[0] != scramble[-1][0]:
					scramble.append(temp)
					break
		turns.extend(["x","y","z"])
		if show_cube_bool:
			visualize(scramble,turns)
		frame.config(text=" ".join(scramble))
def convert(time_):
    time_ = [0,0,time_]
    while time_[2] >= 60:
        time_[2] -= 60
        time_[1] += 1
    while time_[1] >= 60:
        time_[1] -= 60
        time_[0] += 1
    return ":".join(map(str,time_))

show_scramble()
def quit(widget,arg):
	global open_windows
	open_windows[arg] = False
	widget.destroy()
def update_settings():
	global events,times_box_s
	times_box_s.delete(0,END)
	for x,i in zip(range(len(events)),events):
		times_box_s.insert(END,f"{x+1}: {i}")
def event_press(press):
	global event_entry,events,session_drop,shown_info
	if press.char == "\r" and event_entry.get() != "Type an Event" and not event_entry.get().startswith("Inspection time"):
		if add_rem:
			events[event_entry.get()] = []
		else:
			try:
				if len(list(events.keys())) != 1:
					try:
						del events[event_entry.get().title()]
					except KeyError:
						del events[event_entry.get()]
				else:
					raise KeyError
			except KeyError:
				messagebox.showwarning("Event Doesn't Exist","There must be at least one event.\nThe event you typed doesn't exist, thus couldn't be deleted.")
		session_drop.destroy()
		session_drop = OptionMenu(top, var, *tuple(events.keys()),command=change)
		session_drop.grid(row=1,column=0)
		update_settings()
def add(operation):
	global settings_r,event_entry,add_rem
	event_label = Label(settings_r)
	event_label.grid(row=4,column=1,columnspan=2)
	if operation:
		event_label.config(text="  Which event to add?  ")
		add_rem = True
	else:
		event_label.config(text="Which event to remove?")
		add_rem = False
	event_entry = Entry(settings_r)
	event_entry.grid(row=5,column=1,columnspan=2)
	event_entry.insert(0,"Type an Event")
	event_entry.bind("<Key>",event_press)
def inspection_change(change):
	global inspection_time,inspection_time_label,inspection_time_copy
	if change:
		inspection_time += 1
	else:
		if inspection_time >= 2:
			inspection_time -= 1
	inspection_time_label.config(text=f"\nThe inspection time is {inspection_time}s.")
	inspection_time_copy = inspection_time
def inspection_default():
	global inspection_time,inspection_time_default,inspection_time_copy,inspection_time_label
	inspection_time = inspection_time_copy = inspection_time_default
	inspection_time_label.config(text=f"\nThe inspection time is {inspection_time}s.")
def accuracy_change(arg):
	global timer_accuracy,timer_accuracy_label
	if arg == 0:
		timer_accuracy+=1
	elif arg == 1:
		timer_accuracy = 1
	else:
		if timer_accuracy != 1:
			timer_accuracy-=1
	timer_accuracy_label.config(text=f"\nTimer accuracy is {timer_accuracy} ms.")

def change_logo():
	global logo_var,logo_sticker
	logo_sticker = "".join([logo_var.get(),".jpg"])
logo_var = StringVar()
logo_var.set("YJ")
def settings_():
	global settings_r,times_box_s,inspection_time,inspection_time_label,timer_accuracy_label,open_windows,logo_var
	if open_windows[0]:
		return
	open_windows[0] = True
	settings_r = Toplevel()
	settings_r.title("Settings")
	settings_r.iconbitmap("settings_icon.ico")
	settings_r.protocol("WM_DELETE_WINDOW",lambda: quit(settings_r,0))
	settings_r.geometry("260x480")
	settings_label = Label(settings_r,text="These events are set:")
	settings_label.grid(row=1,column=1,columnspan=4)
	settings_close = Button(settings_r,text="Quit",command=lambda: quit(settings_r,0))
	settings_close.grid(row=20,column=1,columnspan=4)
	settings_frame = LabelFrame(settings_r,bd=5)
	settings_frame.grid(row=2,column=1,columnspan=4)
	scrollbar_s = Scrollbar(settings_frame)
	scrollbar_s.pack(side=RIGHT,fill=Y)
	times_box_s = Listbox(settings_frame,yscrollcommand=scrollbar_s.set,width=35)
	times_box_s.pack(side=LEFT,fill=BOTH)
	scrollbar_s.config(command=times_box_s.yview)
	add_event = Button(settings_r,text="Add an Event",command=lambda: add(True),padx=18)
	add_event.grid(row=3,column=1,columnspan=2)
	remove_event = Button(settings_r,text="Remove an Event",command=lambda: add(False),padx=10)
	remove_event.grid(row=3,column=3,columnspan=2)
	inspection_time_whatever = Label(settings_r,text="")
	inspection_time_whatever.grid(row=6,column=1)
	inspection_time_label = Label(settings_r,text=f"\nThe inspection time is {inspection_time}s.")
	inspection_time_label.grid(row=7,column=1,columnspan=4)
	inspection_time_btn_add = Button(settings_r,text="+",padx=15,command=lambda: inspection_change(True))
	inspection_time_btn_add.grid(row=8,column=1)
	inspection_time_btn_default = Button(settings_r,text="Reset",padx=50,command=inspection_default,anchor=W)
	inspection_time_btn_default.grid(row=8,column=2,columnspan=2)
	inspection_time_btn_rem = Button(settings_r,text="-",padx=15,command=lambda: inspection_change(False))
	inspection_time_btn_rem.grid(row=8,column=4)
	timer_accuracy_label = Label(settings_r,text=f"\nTimer accuracy is {timer_accuracy} ms.")
	timer_accuracy_label.grid(row=9,column=1,columnspan=4)
	timer_accuracy_add = Button(settings_r,text="+",padx=15,command=lambda: accuracy_change(0))
	timer_accuracy_add.grid(row=10,column=1)
	timer_accuracy_reset = Button(settings_r,text="Reset",padx=50,command=lambda: accuracy_change(1),anchor=W)
	timer_accuracy_reset.grid(row=10,column=2,columnspan=2)
	timer_accuracy_remove = Button(settings_r,text="-",padx=15,command=lambda: accuracy_change(2))
	timer_accuracy_remove.grid(row=10,column=4)
	cube_brand = LabelFrame(settings_r,text="Cube Brand:",bd=5)
	cube_brand.grid(row=12,column=1,columnspan=4)
	rbs_label = Label(settings_r,text="")
	rbs_label.grid(row=11,column=1)
	logos = [["YJ","MoYu","QiYi"],["YuXin","Gan","Rubik's"]]
	for ia in range(0,2):
		for ib in range(len(logos[ia])):
			rb = Radiobutton(cube_brand,text=logos[ia][ib],value=logos[ia][ib],variable=logo_var,command=change_logo)
			rb.grid(row=ia,column=ib+1)
	update_settings()

def open_link(link):
	webbrowser.open_new(link)
def session_f():
	global session_r,WRs,open_windows
	if open_windows[1]:
		return
	open_windows[1] = True
	wrs_r = Toplevel()
	wrs_r.title("World Records")
	wrs_r.iconbitmap("wca_logo_HvB_icon.ico")
	wrs_r.protocol("WM_DELETE_WINDOW",lambda: quit(wrs_r,1))
	wrs_label = Label(wrs_r,text="World Records")
	wrs_label.grid(row=1)
	wrs_frame = LabelFrame(wrs_r)
	wrs_frame.grid(row=2)
	scrollbar_wrs = Scrollbar(wrs_frame)
	scrollbar_wrs.pack(side=RIGHT,fill=Y)
	times_box_wrs = Listbox(wrs_frame,yscrollcommand=scrollbar_wrs.set,width=40)
	times_box_wrs.pack(side=LEFT,fill=BOTH)
	scrollbar_wrs.config(command=times_box_wrs.yview)
	more_wrs = Button(wrs_r,text="More WRS",command=lambda: open_link("https://www.worldcubeassociation.org/results/records"),padx=40)
	more_wrs.grid(row=3)
	wrs_close = Button(wrs_r,text="Quit",command=lambda: quit(wrs_r,1),padx=40)
	wrs_close.grid(row=4)
	for a,b in WRs.items():
		times_box_wrs.insert(END,f'------ {a} ------')
		times_box_wrs.insert(END,f'Best: {", ".join(map(str, b[0]))}')
		times_box_wrs.insert(END,f'Average: {", ".join(map(str, b[1]))}')
		times_box_wrs.insert(END,"\n")
def bad_file():
	messagebox.showerror("Wrong File","The file you loaded either isn't the save file or the data is corrupted.")
def open_file():
	global file_label,file_dir,events,times_box,session,directory,session_drop,inspection_time_copy,inspection_time,timer_accuracy,logo_sticker
	file = askopenfile(mode ='r',filetypes=[('Save File (.txt)', '*.txt')]) 
	if file is not None:
		try:
			content = file.readlines() 
			if len(content) ==0:
				raise FileNotFoundError
		except (UnicodeDecodeError,FileNotFoundError):
			bad_file()
			return
		file_dir = str(file.name).split("/")[0:len(str(file.name))-1]
		print(content)
		for x,i in zip(range(len(content)),content):
			if i.startswith("Inspection time, timer accuracy"):
				inspection_time,timer_accuracy,logo_sticker = i.split(" = ")[1].split(",")
				inspection_time = int(inspection_time)
				timer_accuracy = int(timer_accuracy)
				inspection_time_copy = inspection_time
				del content[x]
			else:
				content[x] = content[x][0:len(i)-1]
		keys = content[::2]
		del content[::2]
		items = dict.fromkeys(keys)
		for a,b in zip(items.keys(),content):
			items[a] = b
		for a,b in items.items():
			if a != "Events":
				try:
					if len(eval(b)) != 0:
						for i in eval(b):
							try:
								events[a].append(i)
							except KeyError:
								events[a] = eval(b)
								break
					else:
						events[a] = eval(b)
				except (TypeError,SyntaxError):
					bad_file()
					return
		session_drop.destroy()
		session_drop = OptionMenu(top, var, *tuple(events.keys()),command=change)
		session_drop.grid(row=1,column=0)
		show_results()
		directory.config(text="Save File Found")
		#print(f"Inspection time: {inspection_time}")
		del items
		del content
	else:
		bad_file()
def save_file():
	global events,file_dir,directory,sd_label,sd_button_leave,inspection_time_copy,timer_accuracy,logo_sticker
	#print(f"Inspection time: {inspection_time}")
	try:
		file = open("/".join(file_dir),"w")
	except (NameError,NameError):
		file = open(askdirectory()+"Timer Data.txt","w")
	if file is not None:
		file.write("Events\n")
		file.write("['"+"', '".join(events)+"']"+"\n")
		print("--------- SAVING -----------")
		for ia in events:
			file.write(f"{ia}\n")
			if len(events[ia]) != 0:
				file.write("['"+"', '".join(events[ia])+"']"+"\n")
			else:
				file.write("[]\n")
		file.write(f"Inspection time, timer accuracy, logo = {inspection_time_copy},{timer_accuracy},{logo_sticker}")
		file.close()
		directory.config(text="Save File Found")
		sd_label.config(text="Data has been successfully saved.")
		sd_button_leave.config(text="Leave")
		print("\r--------- SAVING -----------")
def close_main_window():
	root.destroy()
def cancel():
	global save_data,open_windows
	open_windows[2] = False
	save_data.destroy()
def close_main_window_save_data():
	global save_data,sd_label,sd_button_leave,open_windows
	if open_windows[2]:
		return
	open_windows[2] = True
	save_data = Toplevel()
	save_data.title("Unsaved Data!")
	save_data.protocol("WM_DELETE_WINDOW",cancel)
	save_data.iconbitmap("settings_icon.ico")
	sd_frame = LabelFrame(save_data,bd=5)
	sd_frame.grid()
	sd_label = Label(sd_frame,text="You might have unsaved data.\nConsider saving it before leaving.")
	sd_label.grid(row=1,column=1,columnspan=3)
	sd_button_save = Button(sd_frame,text="Save data", command=save_file)
	sd_button_save.grid(row=2,column=1)
	sd_button_leave = Button(sd_frame,text="Leave without saving",command=close_main_window)
	sd_button_leave.grid(row=2,column=2)
	sd_button_cancel = Button(sd_frame,text="Cancel",command=cancel)
	sd_button_cancel.grid(row=2,column=3)
def change(value):
	global session,times_box,events,inspection_time,inspection_time_copy,p2s
	print(f"Selected: {value}")
	p2s = False
	session = value
	inspection_time = inspection_time_copy
	show_scramble()
	show_results()
def inspection():
	#messagebox.showinfo("Information","Inspection doesn't work")
	global inspection_bool,inspection_button
	if inspection_bool:
		inspection_bool = False
		inspection_button.config(text="Inspection Off")
	else:
		inspection_bool = True
		inspection_button.config(text="Inspection On")
"""
def dnf():
	pass
"""
def plus2s():
	global events,session,p2s
	try:
		if not p2s:
			events[session][-1] = str(round(float(events[session][-1])+2,3))
			p2s = True
		else:
			events[session][-1] = str(round(float(events[session][-1])-2,3))
			p2s = False
	except IndexError:
		pass
	show_results()
def dnf():
	global events,session,dnf_bool
	try:
		if not dnf_bool:
			events[session][-1] = "DNF"
			dnf_bool = True
		else:
			events[session][-1] = "DNF"
			dnf_bool = False
	except IndexError:
		pass
	show_results()
def remove_solve():
	global events,session
	try:
		del events[session][-1]
		show_results()
	except IndexError:
		pass
def ScrollWindow_Extract(arg):
	global events,session_drop
	evens = arg
	session_drop = OptionMenu(top, var, *tuple(events.keys()),command=change)
	session_drop.grid(row=1,column=0)
def DropDownMenu_extract(arg):
	global session,window
	session = arg
	window.session = arg
class ScrollWindow:
	def __init__(self,dictionary=None,ind=None):
		self.dct = dictionary
		self.session = ind
		self.scrollwindow = Toplevel()
		self.scrollwindow.title("Solves Manager")
		self.scrollwindow.protocol("WM_DELETE_WINDOW",self.quit)
		self.scrollwindow.iconbitmap("settings_icon.ico")
		self.menu = DropDownMenu(self.scrollwindow,items=self.dct,cmd1=self.update_text_box,cmd2=DropDownMenu_extract)
		self.box = TextScroll(self.scrollwindow)
		self.quit_button = Button(self.scrollwindow,text="Quit",command=self.quit)
		self.quit_button.grid(row=5,column=1,columnspan=2)
		self.add = Button(self.scrollwindow,text="Add",command=lambda: self.entry_cmd(True))
		self.add.grid(row=3,column=1)
		self.remove_button = Button(self.scrollwindow,text="Remove",command=lambda: self.entry_cmd(False))
		self.remove_button.grid(row=3,column=2)
		self.update_text_box()
	def update_text_box(self):
		self.box.clear()
		pass
		"""try:
			try: self.fastest = self.dct[self.session].index(str(min(map(float,self.dct[self.session]))))
			except ValueError:
			    try: self.fastest = self.dct[self.session].index("".join([str(min(map(float,self.dct[self.session]))),"0"]))
			    except ValueError:
			        try: self.fastest = self.dct[self.session].index("".join([str(min(map(float,self.dct[self.session]))),"00"]))
			        except ValueError:
			            pass
			try: self.slowest = self.dct[self.session].index(str(max(map(float,self.dct[self.session]))))
			except ValueError:
			    try: self.slowest = self.dct[self.session].index("".join([str(max(map(float,self.dct[self.session]))),"0"]))
			    except ValueError:
			        try: self.slowest = self.dct[self.session].index("".join([str(max(map(float,self.dct[self.session]))),"00"]))
			        except ValueError:
			            pass
			for i,x in zip(list(self.dct[self.session]),range(len(list(self.dct[self.session])))):
				if x == self.fastest:
					self.box.text_box.insert(END,f"{x+1}: {i}s <- BEST")
				elif x == self.slowest and len(self.dct[self.session]) > 1:
					self.box.text_box.insert(END,f"{x+1}: {i}s <- WORST")
				else:
					self.box.text_box.insert(END,f"{x+1}: {i}s")
			show_results()
		except ValueError: pass"""
	def entry_cmd(self,state):
		self.press_arg = state
		self.entry = Entry(self.scrollwindow)
		self.entry.grid(row=4,column=1,columnspan=2)
		if state:
			self.entry.insert(END,"Add an event or time")
			self.entry.bind("<Key>",self.press)
		else:
			self.entry.insert(END,"Remove an event or time")
			self.entry.bind("<Key>",self.press)
	def press(self,key):
		global events,session
		if key.char == "\r":
			if self.dct is not None and self.session is not None:
				if not self.press_arg:
					try:#Remove event
						if len(list(self.dct.values())) != 1:
							del self.dct[self.entry.get()]
							self.menu.tkinter_drop_down_menu.destroy()
							self.menu = DropDownMenu(self.scrollwindow,items=self.dct,cmd1=self.update_text_box,cmd2=DropDownMenu_extract)
							self.update_text_box()
						else:
							messagebox.showwarning("There Must Be At Least One Event","Action couldn't be completed, since there must be at least one event.")
					except (KeyError,AttributeError,ValueError):
						try: #Remove time
							del self.dct[self.session][int(self.entry.get())-1]
							self.update_text_box()
						except (KeyError,AttributeError,ValueError):
							pass
				else:
					try:#Add
						if float(self.entry.get()) > 0:
							self.dct[self.session].append(str(float(self.entry.get())))
							self.update_text_box()
						else:
							messagebox.showwarning("Time Could Not Be Added","The time you just timed couldn't be added. You can't solve anything before you start the timer.")
					except ValueError:
						#print("trying to add something")
						if not self.entry.get().startswith("Inspection time") and not self.entry.get().startswith("Event"):
							self.dct[self.entry.get()] = []
							self.menu.tkinter_drop_down_menu.destroy()
							self.menu = DropDownMenu(self.scrollwindow,items=self.dct,cmd1=self.update_text_box,cmd2=DropDownMenu_extract)
						else:
							messagebox.showwarning("Event Could Not Be Added","No event name can start with 'Event' or 'Inspection time', because it could lead to save data corruption.")
				ScrollWindow_Extract(self.dct)
	def change(state,info):
		pass
	def quit(self):
		global open_windows
		open_windows[3] = False
		self.scrollwindow.destroy()
def solve_manager():
	global events,session,window,open_windows
	if open_windows[3]:
		return
	open_windows[3] = True
	window = ScrollWindow(dictionary=events,ind=session)

def altf4():
	global root
	root.destroy()
def cube_gui_button():
	global show_cube_bool,cube_gui,session,side_length
	if not show_cube_bool:
		show_cube_bool = True
		cube_gui.config(text="Scramble Visualization On")
		try:
			side_length = int(session.split("x")[0])
		except ValueError:
			suppress()
		else:
			visualize(scramble,turns)
	else:
		show_cube_bool = False
		cube_gui.config(text="Scramble Visualization Off")
WRs = {'2x2': [[0.49,"Maciej Czapiewski"],[1.21,"Martin Vædele Egdal"]], '3x3': [[3.47,	"Yusheng Du (杜宇生)"],[5.53,"Feliks Zemdegs"]], '4x4': [[17.42,"Sebastian Weyer"],[21.11,"Max Park"]], '5x5': [[34.92,"Max Park"],[39.65,"Max Park"]], '6x6': [[69.51,"Max Park"],[75.90,"Max Park"]], '7x7': [[100.89,"Max Park"],[106.57,"Max Park"]], 'Skewb': [[0.93,"Andrew Huang"],[2.03,"Łukasz Burliga"]], 'Megaminx': [[27.22,"Juan Pablo Huanqui"],[30.39,"Juan Pablo Huanqui"]], 'Pyraminx': [[0.91,"Dominik Górny"],[1.86,"Tymon Kolasiński"]], 'Clock': [[3.29,"Suen Ming Chi (孫銘志)"],[4.38,"Yunhao Lou (娄云皓)"]], 'Square One': [[4.95,"Jackey Zheng"],[6.54,"Vicenzo Guerino Cecchini"]]}
inspection_bool = False
var = StringVar(top)
var.set("3x3")
session_drop = OptionMenu(top, var, *tuple(events.keys()),command=change)
session_drop.grid(row=1,column=0)
directory = Button(top,text="Save File Not Found",command=open_file)
directory.grid(row=1,column=1)
session_button = Button(top,text="World Records",command=session_f)
session_button.grid(row=1,column=2)
settings = Button(top,text="Settings",command=settings_)
settings.grid(row=1,column=3)
manage_solves = Button(top,text="Manage Solves",command=solve_manager)
manage_solves.grid(row=1,column=4)
cube_gui = Button(top,text="Scramble Visualization Off",command=cube_gui_button)
cube_gui.grid(row=1,column=5)
inspection_button = Button(corner,text="Inspection Off",command=inspection)
inspection_button.grid()
timer = Label(frame,text="0.000s")
timer.config(font=("Times New Roman",100))
timer.grid()
times = []
scrollbar = Scrollbar(left)
scrollbar.pack(side=RIGHT,fill=Y)
times_box = Listbox(left,yscrollcommand=scrollbar.set)
times_box.pack(side=LEFT,fill=BOTH)
scrollbar.config(command=times_box.yview)
inspection_time = 15
inspection_time_copy = inspection_time
"""dnf_button = Button(bottom_buttons,text="DNF",command=dnf)
dnf_button.grid(row=3,column=2,sticky=W)"""
del_button = Button(bottom_buttons,text="Delete",command=remove_solve)
del_button.grid(row=3,column=2,sticky=W)

quit_button=Button(bottom_buttons,text="Alt+F4",command=altf4)
quit_button.grid(row=3,column=8)
p2s = False
dnf_bool = False
plus2s_button = Button(bottom_buttons,text="+2s",command=plus2s)
plus2s_button.grid(row=3,column=3,sticky=W)
inspection_ongoing = False
def display():
	global t0,timer,timer_on,disp,times_label,frame,session,inspection_bool,inspection_time,inspection_ongoing,timer_accuracy
	if timer_on:
		disp = "".join([str(time.time()-t0).split(".")[0],".",str(time.time()-t0).split(".")[1][0:3]])
		timer.config(text=f"{disp}s",bg="green")
		frame.config(bg="green")
		if inspection_bool:
			if inspection_time != 9999999:
				inspection_ongoing = True
			if time.time()-t0 > inspection_time:
				timer_on = False
				timer.config(text="Ready?")
				inspection_ongoing = False
				inspection_time = 9999999
				return
		try:
			timer.after(timer_accuracy,display)
		except RecursionError:
			timer.after(timer_accuracy,display)
def total(x):
	for xi,i in zip(range(len(x)),x):
		x[xi] = float(i)
	return sum(x)
def show_results():
	global times_box,results,session,status
	times_box.delete(0,END)
	"""try:#mohl jsem prostě najít nejmenší čas a při tisku to zohlednit, ne hledat indexy no
		try: fastest = events[session].index(str(min(map(float,events[session]))))
		except ValueError:
		    try: fastest = events[session].index("".join([str(min(map(float,events[session]))),"0"]))
		    except ValueError:
		        try: fastest = events[session].index("".join([str(min(map(float,events[session]))),"00"]))
		        except ValueError:
		            pass
		try: slowest = events[session].index(str(max(map(float,events[session]))))
		except ValueError:
		    try: slowest = events[session].index("".join([str(max(map(float,events[session]))),"0"]))
		    except ValueError:
		        try: slowest = events[session].index("".join([str(max(map(float,events[session]))),"00"]))
		        except ValueError:
		            pass
		for i,x in zip(events[session],range(len(events[session]))):
			if x == fastest:
				times_box.insert(END,f"{x+1}: {i}s <- BEST")
			elif x == slowest and len(events[session]) > 1:
				times_box.insert(END,f"{x+1}: {i}s <- WORST")
			else:
				times_box.insert(END,f"{x+1}: {i}s")
		if len(events[session]) >=100:
			ao100 = round(total(events[session][-100:])/100,3)
			ao50 = round(total(events[session][-50:])/50,3)
			ao12 = round(total(events[session][-12:])/12,3)
			ao5 = round(total(events[session][-5:])/5,3)
			status.config(text=f"Best: {min(events[session])} | Worst: {max(events[session])} | Ao5: {ao5} | Ao12: {ao12} | Ao50: {ao50} | Ao100: {ao100}")
		elif len(events[session]) >=50:
			ao50 = round(total(events[session][-50:])/50,3)
			ao12 = round(total(events[session][-12:])/12,3)
			ao5 = round(total(events[session][-5:])/5,3)
			status.config(text=f"Best: {min(events[session])} | Worst: {max(events[session])} | Ao5: {ao5} | Ao12: {ao12} | Ao50: {ao50} | Ao100: 0")
		elif len(events[session]) >=12:
			ao12 = round(total(events[session][-12:])/12,3)
			ao5 = round(total(events[session][-5:])/5,3)
			status.config(text=f"Best: {min(events[session])} | Worst: {max(events[session])} | Ao5: {ao5} | Ao12: {ao12} | Ao50: 0 | Ao100: 0")
		elif len(events[session]) >=5:
			ao5 = round(total(events[session][-5:])/5,3)
			status.config(text=f"Best: {min(events[session])} | Worst: {max(events[session])} | Ao5: {ao5} | Ao12: 0 | Ao50: 0 | Ao100: 0")
		elif len(events[session]) >=2:
			status.config(text=f"Best: {min(events[session])} | Worst: {max(events[session])} | Ao5: 0 | Ao12: 0 | Ao50: 0 | Ao100: 0")
		elif len(events[session]) ==1:
			status.config(text=f"Best: {min(events[session])} | Worst: 0 | Ao5: 0 | Ao12: 0 | Ao50: 0 | Ao100: 0")
		else:
			status.config(text=f"Best: 0 | Worst: 0 | Ao5: 0 | Ao12: 0 | Ao50: 0 | Ao100: 0")
	except ValueError:
		status.config(text=f"Best: 0 | Worst: 0 | Ao5: 0 | Ao12: 0 | Ao50: 0 | Ao100: 0")"""

def timer_f():
	global timer_on,t0,disp,frame,times,events,session,inspection_time,inspection_time_copy,p2s,inspection_ongoing
	if not timer_on:
		t0 = time.time()
		timer_on = True
		display()
	else:
		timer_on = False
		frame.config(bg="red")
		timer.config(bg="red")

		try:
			if not inspection_ongoing:
				events[session].append(disp)
		except KeyError:
			session = random.choice(list(events.keys()))
			inspection_time = inspection_time_copy
			inspection_ongoing = False
			return
		inspection_ongoing = False
		inspection_time = inspection_time_copy
		p2s = False
		show_results()
def press(btn):
	if str(repr(btn.char)) == "' '":
		timer_f()

timer_on = False
root.bind("<Key>",press)
###########################################
root.protocol("WM_DELETE_WINDOW",close_main_window_save_data)
#messagebox.showinfo("Information","This is a speedsolving timer, which I tried to make as good as possible. \nSo far, it includes:\n▶ Timer\n▶ Loading/Saving your solves\n▶ Adding as many events as you please (NxN cubes, PLL algs...)\n▶ World Records\n▶ Toggleable inspection of custom length\n▶ +2s, deleting and adding solves\n▶ Best time, worst time and averages\n▶ NxN Cube Visualization\n\nSpacebar toggles the timer.\nLoad your data by clicking on the second button from the top left, save it by closing the window.\nThere are two 'solve managers', one in 'Settings' and one in 'Manage Solves'. Both allow you to add and remove events, while 'Solve Manager' also allows you to add and remove times.\n(Solve Manager) If the thing you are trying to add/remove can be converted into a number, the program tries to add/remove a time. If that's not possible, it tries to add/remove an event.\n\n**DO NOT CLOSE THE CONSOLE WINDOW, YOU WILL LOSE YOUR DATA**\n\nIf you encounter an error or simply want to contact me, my Discord Tag is ɹıɥɔuɹn ƃıɐʇǝɹ#7407.")
root.mainloop()
### NEMAZAT
"""
# Config hran a rohů
edges=[
[[0,1],[4,1]], # white-orange   0
[[0,3],[1,1]], # white-green    1
[[0,5],[3,1]], # white-blue     2
[[0,7],[2,1]], # white-red      3
[[1,3],[4,5]], # green-orange   4
[[1,5],[2,3]], # green-red      5
[[2,5],[3,3]], # red-blue       6
[[3,5],[4,3]], # blue-orange    7
[[5,1],[2,7]], # yellow-red     8
[[5,3],[1,7]], # yellow-green   9
[[5,5],[3,7]], # yellow-blue   10
[[5,7],[4,7]]  # yellow-orange 11
]
solved_edges={
str([[0, 1], [4, 1]]):[w,o],
str([[0, 3], [1, 1]]):[w,g],
str([[0, 5], [3, 1]]):[w,b],
str([[0, 7], [2, 1]]):[w,r],
str([[1, 3], [4, 5]]):[g,o],
str([[1, 5], [2, 3]]):[g,r],
str([[2, 5], [3, 3]]):[r,b],
str([[3, 5], [4, 3]]):[b,o],
str([[5, 1], [2, 7]]):[y,r],
str([[5, 3], [1, 7]]):[y,g],
str([[5, 5], [3, 7]]):[y,b],
str([[5, 7], [4, 7]]):[y,o]
}
solved_edges_list=list(solved_edges.keys())
corners=[
[[0,0],[4,2],[1,0]],
[[0,2],[3,2],[4,0]],
[[0,6],[1,2],[2,0]],
[[0,8],[2,2],[3,0]],
[[5,0],[2,6],[1,8]],
[[5,2],[3,6],[2,8]],
[[5,6],[1,6],[4,8]],
[[5,8],[4,6],[3,8]]
]
"""
"""
def visualize(input_scramble,available_turns,f_M,r_M):
	scramble = input_scramble
	global cube_nxn,side_length,r_mid,f_mid,visualization,buttons_root,mod_scramble,moves_done,undone_moves,root
	moves_done=[]
	undone_moves=[]
	turns = available_turns
	f_mid = f_M
	r_mid = r_M
	o = "Orange"
	r = "Red"
	g = "Green"
	b = "Blue"
	y = "Yellow"
	w = "White"
	c = "Cyan"
	mod_scramble = []

	def button_function(arg):
		global moves_done
		moves_done.append(arg)
		s_t0 = time.time()
		do(arg)
		print(f"This took {round(time.time()-s_t0,3)}sec.")
		#show_cube() # Funkce tlačítek
	def do_move(slice1,slice2,slice3,slice4):
		global cube_nxn
		temp = []
		for i in cube_nxn[slice1:slice2]:
			temp.append(i[slice3:slice4])
		temp[0],temp[1],temp[2],temp[3] = temp[1],temp[2],temp[3],temp[0]
		for xa,xc in zip(range(slice1,slice2),range(len(temp))):
			for xb,xd in zip(range(slice3,slice4),range(len(temp[xc]))):
				cube_nxn[xa][xb] = temp[xc][xd] # Slice pohyb (U,D)
	def solve_the_cube(show=True):
		global cube_nxn,side_length
		cube_nxn = [[w]*side_length*side_length,
		[g]*side_length*side_length,
		[r]*side_length*side_length,
		[b]*side_length*side_length,
		[o]*side_length*side_length,
		[y]*side_length*side_length]
		if side_length == 1:
			cube_nxn[0][0] == c
		if side_length%2 == 0:
			cube_nxn[0][side_length+1] = c
		else:
			cube_nxn[0][round(side_length**2-side_length**2/2)] = c
		if show:
			show_cube() # Vytvořit kostku
	def reset_the_cube():
		global scramble
		s_t0 = time.time()
		solve_the_cube(show=False)
		for i in scramble:
			do(i)
		show_cube()
		print(f"This took {round(time.time()-s_t0,3)}sec.") #  # Resetovat scramble
	def rotate_face(slc):
		global cube_nxn,side_length
		lst = []
		lst_ = cube_nxn[slc]
		for i in range(side_length):
			lst.append(lst_[side_length*i:side_length*(i+1)])
		lst_ = []
		lst_ = [list(reversed(col)) for col in zip(*lst)]
		lst = []
		for i in lst_:
			lst.extend(i)
		cube_nxn[slc] = lst
		#cube_nxn[i][0],cube_nxn[i][1],cube_nxn[i][2],cube_nxn[i][3],cube_nxn[i][4],cube_nxn[i][5],cube_nxn[i][6],cube_nxn[i][7],cube_nxn[i][8] = cube_nxn[i][2],cube_nxn[i][5],cube_nxn[i][8],cube_nxn[i][1],cube_nxn[i][4],cube_nxn[i][7],cube_nxn[i][0],cube_nxn[i][3],cube_nxn[i][6] # Otočení vrchu
	def do(turn,show=True):
		global cuben_nxn,side_length,r_mid,f_mid
		s1 = side_length**2-side_length
		s2 = side_length**2
		if turn == "U":
			do_move(1,5,0,side_length)
			rotate_face(0)
		elif turn == "U2":
			do_move(1,5,0,side_length)
			do_move(1,5,0,side_length)
			rotate_face(0)
			rotate_face(0)
		elif turn == "U'":
			do_move(1,5,0,side_length)
			do_move(1,5,0,side_length)
			do_move(1,5,0,side_length)
			rotate_face(0)
			rotate_face(0)
			rotate_face(0)
		elif turn == "D'":
			do_move(1,5,side_length*side_length-side_length,side_length*side_length)
			rotate_face(5)
			rotate_face(5)
			rotate_face(5)
		elif turn == "D2":
			do_move(1,5,side_length*side_length-side_length,side_length*side_length)
			do_move(1,5,side_length*side_length-side_length,side_length*side_length)
			rotate_face(5)
			rotate_face(5)
		elif turn == "D":
			do_move(1,5,side_length*side_length-side_length,side_length*side_length)
			do_move(1,5,side_length*side_length-side_length,side_length*side_length)
			do_move(1,5,side_length*side_length-side_length,side_length*side_length)
			rotate_face(5)
		elif turn == "F":
			cube_nxn[0][side_length**2-side_length:side_length**2],cube_nxn[3][0::side_length],cube_nxn[5][0:side_length],cube_nxn[1][side_length-1::side_length] = cube_nxn[1][side_length-1::side_length],list(reversed(cube_nxn[0][side_length**2-side_length:side_length**2])),cube_nxn[3][0::side_length],list(reversed(cube_nxn[5][0:side_length]))
			rotate_face(2)
			cube_nxn[0][side_length**2-side_length:side_length**2] = list(reversed(cube_nxn[0][side_length**2-side_length:side_length**2]))
			cube_nxn[5][0:side_length] = list(reversed(cube_nxn[5][0:side_length]))
			cube_nxn[3][0::side_length] = list(reversed(cube_nxn[3][0::side_length]))
			cube_nxn[1][side_length-1::side_length] = list(reversed(cube_nxn[1][side_length-1::side_length]))
		elif turn == "F2":
			cube_nxn[0][side_length**2-side_length:side_length**2],cube_nxn[3][0::side_length],cube_nxn[5][0:side_length],cube_nxn[1][side_length-1::side_length] = cube_nxn[1][side_length-1::side_length],cube_nxn[0][side_length**2-side_length:side_length**2],cube_nxn[3][0::side_length],cube_nxn[5][0:side_length]
			cube_nxn[0][side_length**2-side_length:side_length**2],cube_nxn[3][0::side_length],cube_nxn[5][0:side_length],cube_nxn[1][side_length-1::side_length] = cube_nxn[1][side_length-1::side_length],cube_nxn[0][side_length**2-side_length:side_length**2],cube_nxn[3][0::side_length],cube_nxn[5][0:side_length]
			rotate_face(2)
			rotate_face(2)
			cube_nxn[0][side_length**2-side_length:side_length**2] = list(reversed(cube_nxn[0][side_length**2-side_length:side_length**2]))
			cube_nxn[5][0:side_length] = list(reversed(cube_nxn[5][0:side_length]))
			cube_nxn[3][0::side_length] = list(reversed(cube_nxn[3][0::side_length]))
			cube_nxn[1][side_length-1::side_length] = list(reversed(cube_nxn[1][side_length-1::side_length]))
		elif turn == "F'":
			cube_nxn[0][side_length**2-side_length:side_length**2],cube_nxn[3][0::side_length],cube_nxn[5][0:side_length],cube_nxn[1][side_length-1::side_length] = cube_nxn[1][side_length-1::side_length],cube_nxn[0][side_length**2-side_length:side_length**2],cube_nxn[3][0::side_length],cube_nxn[5][0:side_length]
			cube_nxn[0][side_length**2-side_length:side_length**2],cube_nxn[3][0::side_length],cube_nxn[5][0:side_length],cube_nxn[1][side_length-1::side_length] = cube_nxn[1][side_length-1::side_length],cube_nxn[0][side_length**2-side_length:side_length**2],cube_nxn[3][0::side_length],cube_nxn[5][0:side_length]
			cube_nxn[0][side_length**2-side_length:side_length**2],cube_nxn[3][0::side_length],cube_nxn[5][0:side_length],cube_nxn[1][side_length-1::side_length] = cube_nxn[1][side_length-1::side_length],cube_nxn[0][side_length**2-side_length:side_length**2],cube_nxn[3][0::side_length],cube_nxn[5][0:side_length]
			rotate_face(2)
			rotate_face(2)
			rotate_face(2)
			cube_nxn[3][0::side_length] = list(reversed(cube_nxn[3][0::side_length]))
			cube_nxn[1][side_length-1::side_length] = list(reversed(cube_nxn[1][side_length-1::side_length]))
		elif turn == "B'":
			cube_nxn[0][0:side_length],cube_nxn[3][side_length-1::side_length],cube_nxn[5][side_length**2-side_length:side_length**2],cube_nxn[1][0::side_length] = cube_nxn[1][0::side_length],cube_nxn[0][0:side_length],cube_nxn[3][side_length-1::side_length],cube_nxn[5][side_length**2-side_length:side_length**2]
			rotate_face(4)
			rotate_face(4)
			rotate_face(4)
			cube_nxn[0][0:side_length] = list(reversed(cube_nxn[0][0:side_length]))
			cube_nxn[5][side_length**2-side_length:side_length**2] = list(reversed(cube_nxn[5][side_length**2-side_length:side_length**2]))
		elif turn == "B2":
			cube_nxn[0][0:side_length],cube_nxn[3][side_length-1::side_length],cube_nxn[5][side_length**2-side_length:side_length**2],cube_nxn[1][0::side_length] = cube_nxn[1][0::side_length],cube_nxn[0][0:side_length],cube_nxn[3][side_length-1::side_length],cube_nxn[5][side_length**2-side_length:side_length**2]
			cube_nxn[0][0:side_length],cube_nxn[3][side_length-1::side_length],cube_nxn[5][side_length**2-side_length:side_length**2],cube_nxn[1][0::side_length] = cube_nxn[1][0::side_length],cube_nxn[0][0:side_length],cube_nxn[3][side_length-1::side_length],cube_nxn[5][side_length**2-side_length:side_length**2]
			rotate_face(4)
			rotate_face(4)
			cube_nxn[0][0:side_length] = list(reversed(cube_nxn[0][0:side_length]))
			cube_nxn[3][side_length-1::side_length] = list(reversed(cube_nxn[3][side_length-1::side_length]))
			cube_nxn[5][side_length**2-side_length:side_length**2] = list(reversed(cube_nxn[5][side_length**2-side_length:side_length**2]))
			cube_nxn[1][0::side_length] = list(reversed(cube_nxn[1][0::side_length]))
		elif turn == "B":
			cube_nxn[0][0:side_length],cube_nxn[3][side_length-1::side_length],cube_nxn[5][side_length**2-side_length:side_length**2],cube_nxn[1][0::side_length] = cube_nxn[1][0::side_length],cube_nxn[0][0:side_length],cube_nxn[3][side_length-1::side_length],cube_nxn[5][side_length**2-side_length:side_length**2]
			cube_nxn[0][0:side_length],cube_nxn[3][side_length-1::side_length],cube_nxn[5][side_length**2-side_length:side_length**2],cube_nxn[1][0::side_length] = cube_nxn[1][0::side_length],cube_nxn[0][0:side_length],cube_nxn[3][side_length-1::side_length],cube_nxn[5][side_length**2-side_length:side_length**2]
			cube_nxn[0][0:side_length],cube_nxn[3][side_length-1::side_length],cube_nxn[5][side_length**2-side_length:side_length**2],cube_nxn[1][0::side_length] = cube_nxn[1][0::side_length],cube_nxn[0][0:side_length],cube_nxn[3][side_length-1::side_length],cube_nxn[5][side_length**2-side_length:side_length**2]
			rotate_face(4)
			cube_nxn[3][side_length-1::side_length] = list(reversed(cube_nxn[3][side_length-1::side_length]))
			cube_nxn[1][0::side_length] = list(reversed(cube_nxn[1][0::side_length]))
		elif turn == "R":
			cube_nxn[0][side_length-1::side_length],cube_nxn[2][side_length-1::side_length],cube_nxn[4][0::side_length],cube_nxn[5][side_length-1::side_length] = cube_nxn[2][side_length-1::side_length],cube_nxn[5][side_length-1::side_length],cube_nxn[0][side_length-1::side_length],cube_nxn[4][0::side_length]
			rotate_face(3)
			cube_nxn[5][side_length-1::side_length] = list(reversed(cube_nxn[5][side_length-1::side_length]))
			cube_nxn[4][0::side_length] = list(reversed(cube_nxn[4][0::side_length]))
		elif turn == "R2":
			cube_nxn[0][side_length-1::side_length],cube_nxn[2][side_length-1::side_length],cube_nxn[4][0::side_length],cube_nxn[5][side_length-1::side_length] = cube_nxn[5][side_length-1::side_length],cube_nxn[4][0::side_length],cube_nxn[2][side_length-1::side_length],cube_nxn[0][side_length-1::side_length]
			rotate_face(3)
			rotate_face(3)
			cube_nxn[4][0::side_length] = list(reversed(cube_nxn[4][0::side_length]))
			cube_nxn[2][side_length-1::side_length] = list(reversed(cube_nxn[2][side_length-1::side_length]))
		elif turn == "R'":
			cube_nxn[0][side_length-1::side_length],cube_nxn[2][side_length-1::side_length],cube_nxn[5][side_length-1::side_length],cube_nxn[4][0::side_length] = cube_nxn[4][0::side_length],cube_nxn[0][side_length-1::side_length],cube_nxn[2][side_length-1::side_length],cube_nxn[5][side_length-1::side_length]
			rotate_face(3)
			rotate_face(3)
			rotate_face(3)
			cube_nxn[0][side_length-1::side_length] = list(reversed(cube_nxn[0][side_length-1::side_length]))
			cube_nxn[4][0::side_length] = list(reversed(cube_nxn[4][0::side_length]))
		elif turn == "L'":
			cube_nxn[0][0::side_length],cube_nxn[2][0::side_length],cube_nxn[4][side_length-1::side_length],cube_nxn[5][0::side_length]	= cube_nxn[2][0::side_length],cube_nxn[5][0::side_length],cube_nxn[0][0::side_length],cube_nxn[4][side_length-1::side_length]
			rotate_face(1)
			rotate_face(1)
			rotate_face(1)
			cube_nxn[5][0::side_length] = list(reversed(cube_nxn[5][0::side_length]))
			cube_nxn[4][side_length-1::side_length] = list(reversed(cube_nxn[4][side_length-1::side_length]))
		elif turn == "L2":
			cube_nxn[0][0::side_length],cube_nxn[2][0::side_length],cube_nxn[4][side_length-1::side_length],cube_nxn[5][0::side_length] = cube_nxn[5][0::side_length],cube_nxn[4][side_length-1::side_length],cube_nxn[2][0::side_length],cube_nxn[0][0::side_length]
			rotate_face(1)
			rotate_face(1)
			cube_nxn[2][0::side_length] = list(reversed(cube_nxn[2][0::side_length]))
			cube_nxn[4][side_length-1::side_length] = list(reversed(cube_nxn[4][side_length-1::side_length]))
		elif turn == "L":
			cube_nxn[0][0::side_length],cube_nxn[2][0::side_length],cube_nxn[4][side_length-1::side_length],cube_nxn[5][0::side_length]	= cube_nxn[4][side_length-1::side_length],cube_nxn[0][0::side_length],cube_nxn[5][0::side_length],cube_nxn[2][0::side_length]
			rotate_face(1)
			cube_nxn[0][0::side_length] = list(reversed(cube_nxn[0][0::side_length]))
			cube_nxn[4][side_length-1::side_length] = list(reversed(cube_nxn[4][side_length-1::side_length]))
		elif turn == "E":
			do_move(1,5,side_length,side_length*side_length-side_length)
			do_move(1,5,side_length,side_length*side_length-side_length)
			do_move(1,5,side_length,side_length*side_length-side_length)
		elif turn == "E2":
			do_move(1,5,side_length,side_length*side_length-side_length)
			do_move(1,5,side_length,side_length*side_length-side_length)
		elif turn == "E'":
			do_move(1,5,side_length,side_length*side_length-side_length)
		elif turn == "y":
			#Why not   cube_nxn[1],cube_nxn[2],cube_nxn[3],cube_nxn[4] = cube_nxn[2],cube_nxn[3],cube_nxn[4],cube_nxn[1] | rotate_face(0) | rotate_face(5)   ?
			do("E'",show=False)
			do("U",show=False)
			do("D'",show=False)
		elif turn == "x":
			do("R",show=False)
			do("L'",show=False)
			for i in r_mid:
				do(i,show=False)
		elif turn == "z":
			do("F",show=False)
			do("B'",show=False)
			for i in f_mid:
				do(i,show=False)
		else:
				try:
					x = turn.split("U")
					if len(x) == 1:
						raise IndexError
					do_move(1,5,(int(x[0])-1)*side_length,int(x[0])*side_length)
					if x[1] == "'":
						do_move(1,5,(int(x[0])-1)*side_length,int(x[0])*side_length)
						do_move(1,5,(int(x[0])-1)*side_length,int(x[0])*side_length)
					elif x[1] == "2":
						do_move(1,5,(int(x[0])-1)*side_length,int(x[0])*side_length)
				except IndexError:
					try:
						
						y = turn.split("F")
						if len(y) == 1:
							raise IndexError
						x = int(y[0])
						if y[1] == "'":
							rotate_face(0)
							rotate_face(0)
							rotate_face(1)
							rotate_face(1)
							cube_nxn[3][x-1::side_length] = list(reversed(cube_nxn[3][x-1::side_length]))
							cube_nxn[1][x-1::side_length] = list(reversed(cube_nxn[1][x-1::side_length]))
							cube_nxn[0][side_length*(x-1):side_length*x],cube_nxn[3][x-1::side_length],cube_nxn[5][side_length*(x-1):side_length*x],cube_nxn[1][x-1::side_length] = cube_nxn[3][x-1::side_length],cube_nxn[5][side_length*(x-1):side_length*x],cube_nxn[1][x-1::side_length],cube_nxn[0][side_length*(x-1):side_length*x]
							cube_nxn[3][x-1::side_length] = list(reversed(cube_nxn[3][x-1::side_length]))
							cube_nxn[1][x-1::side_length] = list(reversed(cube_nxn[1][x-1::side_length]))
							rotate_face(1)
							rotate_face(1)
							rotate_face(0)
							rotate_face(0)
						elif y[1] == "":
							rotate_face(0)
							rotate_face(0)
							rotate_face(1)
							rotate_face(1)
							cube_nxn[3][x-1::side_length] = list(reversed(cube_nxn[3][x-1::side_length]))
							cube_nxn[1][x-1::side_length] = list(reversed(cube_nxn[1][x-1::side_length]))
							cube_nxn[0][side_length*(x-1):side_length*x],cube_nxn[3][x-1::side_length],cube_nxn[5][side_length*(x-1):side_length*x],cube_nxn[1][x-1::side_length] = cube_nxn[3][x-1::side_length],cube_nxn[5][side_length*(x-1):side_length*x],cube_nxn[1][x-1::side_length],cube_nxn[0][side_length*(x-1):side_length*x]
							cube_nxn[0][side_length*(x-1):side_length*x],cube_nxn[3][x-1::side_length],cube_nxn[5][side_length*(x-1):side_length*x],cube_nxn[1][x-1::side_length] = cube_nxn[3][x-1::side_length],cube_nxn[5][side_length*(x-1):side_length*x],cube_nxn[1][x-1::side_length],cube_nxn[0][side_length*(x-1):side_length*x]
							cube_nxn[0][side_length*(x-1):side_length*x],cube_nxn[3][x-1::side_length],cube_nxn[5][side_length*(x-1):side_length*x],cube_nxn[1][x-1::side_length] = cube_nxn[3][x-1::side_length],cube_nxn[5][side_length*(x-1):side_length*x],cube_nxn[1][x-1::side_length],cube_nxn[0][side_length*(x-1):side_length*x]
							cube_nxn[3][x-1::side_length] = list(reversed(cube_nxn[3][x-1::side_length]))
							cube_nxn[1][x-1::side_length] = list(reversed(cube_nxn[1][x-1::side_length]))
							rotate_face(0)
							rotate_face(0)
							rotate_face(1)
							rotate_face(1)
						else:
							rotate_face(0)
							rotate_face(0)
							rotate_face(1)
							rotate_face(1)
							cube_nxn[3][x-1::side_length] = list(reversed(cube_nxn[3][x-1::side_length]))
							cube_nxn[1][x-1::side_length] = list(reversed(cube_nxn[1][x-1::side_length]))
							cube_nxn[0][side_length*(x-1):side_length*x],cube_nxn[3][x-1::side_length],cube_nxn[5][side_length*(x-1):side_length*x],cube_nxn[1][x-1::side_length] = cube_nxn[3][x-1::side_length],cube_nxn[5][side_length*(x-1):side_length*x],cube_nxn[1][x-1::side_length],cube_nxn[0][side_length*(x-1):side_length*x]
							cube_nxn[0][side_length*(x-1):side_length*x],cube_nxn[3][x-1::side_length],cube_nxn[5][side_length*(x-1):side_length*x],cube_nxn[1][x-1::side_length] = cube_nxn[3][x-1::side_length],cube_nxn[5][side_length*(x-1):side_length*x],cube_nxn[1][x-1::side_length],cube_nxn[0][side_length*(x-1):side_length*x]
							cube_nxn[3][x-1::side_length] = list(reversed(cube_nxn[3][x-1::side_length]))
							cube_nxn[1][x-1::side_length] = list(reversed(cube_nxn[1][x-1::side_length]))
							rotate_face(0)
							rotate_face(0)
							rotate_face(1)
							rotate_face(1)
					except IndexError:
						y = turn.split("L")
						x = int(y[0])
						if y[1] == "'":
							rotate_face(4)
							rotate_face(4)
							cube_nxn[0][x-1::side_length],cube_nxn[2][x-1::side_length],cube_nxn[5][x-1::side_length],cube_nxn[4][x-1::side_length] = cube_nxn[2][x-1::side_length],cube_nxn[5][x-1::side_length],cube_nxn[4][x-1::side_length],cube_nxn[0][x-1::side_length]
							rotate_face(4)
							rotate_face(4)
						elif y[1] == "":
							rotate_face(4)
							rotate_face(4)
							cube_nxn[0][x-1::side_length],cube_nxn[2][x-1::side_length],cube_nxn[5][x-1::side_length],cube_nxn[4][x-1::side_length] = cube_nxn[2][x-1::side_length],cube_nxn[5][x-1::side_length],cube_nxn[4][x-1::side_length],cube_nxn[0][x-1::side_length]
							cube_nxn[0][x-1::side_length],cube_nxn[2][x-1::side_length],cube_nxn[5][x-1::side_length],cube_nxn[4][x-1::side_length] = cube_nxn[2][x-1::side_length],cube_nxn[5][x-1::side_length],cube_nxn[4][x-1::side_length],cube_nxn[0][x-1::side_length]
							cube_nxn[0][x-1::side_length],cube_nxn[2][x-1::side_length],cube_nxn[5][x-1::side_length],cube_nxn[4][x-1::side_length] = cube_nxn[2][x-1::side_length],cube_nxn[5][x-1::side_length],cube_nxn[4][x-1::side_length],cube_nxn[0][x-1::side_length]
							rotate_face(4)
							rotate_face(4)
						else:
							rotate_face(4)
							rotate_face(4)
							cube_nxn[0][x-1::side_length],cube_nxn[2][x-1::side_length],cube_nxn[5][x-1::side_length],cube_nxn[4][x-1::side_length] = cube_nxn[2][x-1::side_length],cube_nxn[5][x-1::side_length],cube_nxn[4][x-1::side_length],cube_nxn[0][x-1::side_length]
							cube_nxn[0][x-1::side_length],cube_nxn[2][x-1::side_length],cube_nxn[5][x-1::side_length],cube_nxn[4][x-1::side_length] = cube_nxn[2][x-1::side_length],cube_nxn[5][x-1::side_length],cube_nxn[4][x-1::side_length],cube_nxn[0][x-1::side_length]
							rotate_face(4)
							rotate_face(4)
		if show:
			show_cube() # Otočení R,L,F,B
	def quit():
		global visualization,buttons_root
		visualization.destroy()
		buttons_root.destroy()
		global root
		root.destroy() # Vypnout program při kliknutí na křížek
	def show_cube():
		global logo,logo_sticker,side_length
		from PIL import ImageTk,Image
		logo = ImageTk.PhotoImage(Image.open(logo_sticker).resize((30, 35), Image.ANTIALIAS))
		for i in visualization.winfo_children():
			i.destroy()
		ind = 0
		for ia in range(1,side_length+1):
			for ib in range(side_length+1,side_length*2+1):
				a = LabelFrame(visualization,bd=5)
				a.grid(row=ia,column=ib)
				if cube_nxn[0][ind] == "Cyan":
					b = Label(a,image=logo,padx=15,pady=10,bd=5)
				else:
					b = Label(a,bg=cube_nxn[0][ind].lower(),padx=15,pady=10,bd=5)
				b.grid()
				ind+=1
		ind = 0
		for ia in range(side_length+1,side_length*2+1):
			for ib in range(1,side_length+1):
				a = LabelFrame(visualization,bd=5)
				a.grid(row=ia,column=ib)
				if cube_nxn[1][ind] == "Cyan":
					b = Label(a,image=logo,padx=15,pady=10,bd=5)
				else:
					b = Label(a,bg=cube_nxn[1][ind].lower(),padx=15,pady=10,bd=5)
				b.grid()
				ind+=1
		ind = 0
		for ia in range(side_length*2+1,side_length*3+1):
			for ib in range(side_length+1,side_length*2+1):
				a = LabelFrame(visualization,bd=5)
				a.grid(row=ia,column=ib)
				if cube_nxn[5][ind] == "Cyan":
					b = Label(a,image=logo,padx=15,pady=10,bd=5)
				else:
					b = Label(a,bg=cube_nxn[5][ind].lower(),padx=15,pady=10,bd=5)
				b.grid()
				ind+=1
		ind = 0
		for ia in range(side_length+1,side_length*2+1):
			for ib in range(side_length+1,side_length*2+1):
				a = LabelFrame(visualization,bd=5)
				a.grid(row=ia,column=ib)
				if cube_nxn[2][ind] == "Cyan":
					b = Label(a,image=logo,padx=15,pady=10,bd=5)
				else:
					b = Label(a,bg=cube_nxn[2][ind].lower(),padx=15,pady=10,bd=5)
				b.grid()
				ind+=1
		ind = 0
		for ia in range(side_length+1,side_length*2+1):
			for ib in range(side_length*2+1,side_length*3+1):
				a = LabelFrame(visualization,bd=5)
				a.grid(row=ia,column=ib)
				if cube_nxn[3][ind] == "Cyan":
					b = Label(a,image=logo,padx=15,pady=10,bd=5)
				else:
					b = Label(a,bg=cube_nxn[3][ind].lower(),padx=15,pady=10,bd=5)
				b.grid()
				ind+=1
		ind = 0
		for ia in range(side_length+1,side_length*2+1):
			for ib in range(side_length*3+1,side_length*4+1):
				a = LabelFrame(visualization,bd=5)
				a.grid(row=ia,column=ib)
				if cube_nxn[4][ind] == "Cyan":
					b = Label(a,image=logo,padx=15,pady=10,bd=5)
				else:
					b = Label(a,bg=cube_nxn[4][ind].lower(),padx=15,pady=10,bd=5)
				b.grid()
				ind+=1 # Zobrazit kostku
	def undo(move):
		global moves_done,undone_moves
		try:
			last_move=moves_done[-1]
			do(last_move)
			do(last_move)
			do(last_move)
			del moves_done[-1]
			undone_moves.append(last_move)
		except:pass # Tlačítka - undo
	def redo(move):
		global moves_done,undone_moves
		try:
			last_move=undone_moves[-1]
			do(last_move)
			del undone_moves[-1]
			moves_done.append(last_move)
		except:pass# Tlačítka - redo
	def rndsc():
		global turns
		scramble=[]
		scramble.append(random.choice(turns))
		for i in range(0,random.randint(side_length*10-side_length,side_length*10)):
			while True:
				temp = random.choice(turns)
				if temp[0] != scramble[-1][0]:
					scramble.append(temp)
					break
		print(scramble)
		for i in scramble:
			do(i,show=0)
		show_cube()# Tlačítka - zamíchání kostky
	def buttons_gui(): # Panel tlačítek
		global buttons_root,side_length,mod_scramble
		turns_buttons=deepcopy(turns)
		max_len=len(str(max(turns_buttons,key=len)))
		for x in range(len(turns_buttons)):
			turn_len=len(turns_buttons[x])
			if turn_len!=max_len:
				turns_buttons[x]=turns_buttons[x]+" "*(max_len-turn_len)
		buttons_root = Toplevel()
		buttons_root.title("These Moves Can Be Applied:")
		buttons_root.iconbitmap("rubiks_cube_icon.ico")
		buttons_root.protocol("WM_DELETE_WINDOW",quit)
		buttons = LabelFrame(buttons_root,bd=10)
		buttons.grid()
		ind = 0
		rw = 1
		for txt,i in zip(turns_buttons,turns):
			
			if side_length == 3:
				if i.startswith("2L"):
					i = i.replace("2L","M")
				elif i.startswith("2U"):
					i = i.replace("2U","E")
				elif i.startswith("2F"):
					i = i.replace("2F","S")
			
			mod_scramble.append(i)
			btn = Button(buttons,text=txt,command=lambda var=i: button_function(var))
			btn.grid(row=rw,column=ind)
			ind+=1
			if ind == 20:
				ind = 0
				rw+=1

		reset_the_cube_button = Button(buttons,text="Reset",command=reset_the_cube).grid(row=rw+1,column=0,columnspan=2)
		solve_the_cube_button = Button(buttons,text="Solve",command=solve_the_cube).grid(row=rw+1,column=2,columnspan=2)
		undo_button = Button(buttons,text="Undo ",command=lambda var=txt: undo(var)).grid(row=rw+1,column=4,columnspan=2)
		redo_button = Button(buttons,text="Redo ",command=lambda var=txt: redo(var)).grid(row=rw+1,column=6,columnspan=2)
		random_scramble_button = Button(buttons,text="RNDSC",command=rndsc).grid(row=rw+1,column=8,columnspan=2)
		quit_button = Button(buttons,text="Quit ",command=quit).grid(row=rw+1,column=10,columnspan=2)
	solve_the_cube(show=False)
	buttons_gui()
	visualization = Toplevel()
	visualization.iconbitmap("rubiks_cube_icon.ico")
	visualization.protocol("WM_DELETE_WINDOW",quit)
	visualization.title(" ".join(input_scramble))
	#s_t0 = time.time()
	for i in scramble:	
		do(i)
	show_cube()
"""

### Visualization 2
"""def visualize(input_scramble,available_turns,f_M,r_M):
	scramble = input_scramble
	scramble=["U'","R","2L2"]
	global cube_nxn,side_length,r_mid,f_mid,visualization,buttons_root,moves_done,undone_moves,root
	moves_done=[]
	undone_moves=[]
	turns = available_turns
	f_mid = f_M
	r_mid = r_M
	o = "Orange"
	r = "Red"
	g = "Green"
	b = "Blue"
	y = "Yellow"
	w = "White"
	c = "Cyan"

	def button_function(arg):
		global moves_done
		moves_done.append(arg)
		do(arg)
		#show_cube() # Funkce tlačítek
	def do_move(slice3,slice4,shift): # U,D pohyby, SLICE POHYBY U 4X4+ SE NEMUSÍ ZOBRAZOVAT SPRÁVNĚ KVŮLI TŘETÍMU PARAMETRU

		global cube_nxn
		slice_colors=[]
		for i in cube_nxn[1:5]:
			slice_colors.append(i[slice3:slice4])
		slice_colors=slice_colors[shift:]+slice_colors[:shift]
		for xa,xc in zip(range(1,5),range(len(slice_colors))):
			for xb,xd in zip(range(slice3,slice4),range(len(slice_colors[xc]))):
				cube_nxn[xa][xb] = slice_colors[xc][xd] # Slice pohyb (U,D)
	def solve_the_cube(show=True):
		global cube_nxn,side_length
		cube_nxn = [[w]*side_length*side_length,
		[g]*side_length*side_length,
		[r]*side_length*side_length,
		[b]*side_length*side_length,
		[o]*side_length*side_length,
		[y]*side_length*side_length]
		if side_length == 1:
			cube_nxn[0][0] == c
		if side_length%2 == 0:
			cube_nxn[0][side_length+1] = c
		else:
			cube_nxn[0][round(side_length**2-side_length**2/2)] = c
		if show:
			show_cube() # Vytvořit kostku
	def reset_the_cube():
		global scramble
		solve_the_cube(show=False)
		for i in scramble:
			do(i)
		show_cube()
	def rotate_face(slc):
		global cube_nxn,side_length
		cube_nxn[slc] = sum([list(reversed(cube_nxn[slc][i::side_length])) for i in range(side_length)],[])
	def do(turn,show=True):
		def reverse_str(item):
			return list(reversed(item))
		global cuben_nxn,side_length,r_mid,f_mid
		s1 = side_length**2-side_length
		s2 = side_length**2
		if turn == "U":
			do_move(0,side_length,1)
			rotate_face(0)
		elif turn == "U2":
			do_move(0,side_length,2)
			rotate_face(0)
			rotate_face(0)
		elif turn == "U'":
			do_move(0,side_length,3)
			rotate_face(0)
			rotate_face(0)
			rotate_face(0)
		elif turn == "D'":
			do_move(side_length*side_length-side_length,side_length*side_length,1)
			rotate_face(5)
			rotate_face(5)
			rotate_face(5)
		elif turn == "D2":
			do_move(side_length*side_length-side_length,side_length*side_length,2)
			rotate_face(5)
			rotate_face(5)
		elif turn == "D":
			do_move(side_length*side_length-side_length,side_length*side_length,3)
			rotate_face(5)
		elif turn == "F":
			cube_nxn[0][side_length**2-side_length:side_length**2],cube_nxn[3][0::side_length],cube_nxn[5][0:side_length],cube_nxn[1][side_length-1::side_length] = cube_nxn[1][side_length-1::side_length],list(reversed(cube_nxn[0][side_length**2-side_length:side_length**2])),cube_nxn[3][0::side_length],list(reversed(cube_nxn[5][0:side_length]))
			rotate_face(2)
			cube_nxn[0][side_length**2-side_length:side_length**2] = list(reversed(cube_nxn[0][side_length**2-side_length:side_length**2]))
			cube_nxn[5][0:side_length] = list(reversed(cube_nxn[5][0:side_length]))
			cube_nxn[3][0::side_length] = list(reversed(cube_nxn[3][0::side_length]))
			cube_nxn[1][side_length-1::side_length] = list(reversed(cube_nxn[1][side_length-1::side_length]))
		elif turn == "F2":
			cube_nxn[0][side_length**2-side_length:side_length**2],cube_nxn[3][0::side_length],cube_nxn[5][0:side_length],cube_nxn[1][side_length-1::side_length] = cube_nxn[1][side_length-1::side_length],cube_nxn[0][side_length**2-side_length:side_length**2],cube_nxn[3][0::side_length],cube_nxn[5][0:side_length]
			cube_nxn[0][side_length**2-side_length:side_length**2],cube_nxn[3][0::side_length],cube_nxn[5][0:side_length],cube_nxn[1][side_length-1::side_length] = cube_nxn[1][side_length-1::side_length],cube_nxn[0][side_length**2-side_length:side_length**2],cube_nxn[3][0::side_length],cube_nxn[5][0:side_length]
			rotate_face(2)
			rotate_face(2)
			cube_nxn[0][side_length**2-side_length:side_length**2] = list(reversed(cube_nxn[0][side_length**2-side_length:side_length**2]))
			cube_nxn[5][0:side_length] = list(reversed(cube_nxn[5][0:side_length]))
			cube_nxn[3][0::side_length] = list(reversed(cube_nxn[3][0::side_length]))
			cube_nxn[1][side_length-1::side_length] = list(reversed(cube_nxn[1][side_length-1::side_length]))
		elif turn == "F'":
			cube_nxn[0][side_length**2-side_length:side_length**2],cube_nxn[3][0::side_length],cube_nxn[5][0:side_length],cube_nxn[1][side_length-1::side_length] = cube_nxn[1][side_length-1::side_length],cube_nxn[0][side_length**2-side_length:side_length**2],cube_nxn[3][0::side_length],cube_nxn[5][0:side_length]
			cube_nxn[0][side_length**2-side_length:side_length**2],cube_nxn[3][0::side_length],cube_nxn[5][0:side_length],cube_nxn[1][side_length-1::side_length] = cube_nxn[1][side_length-1::side_length],cube_nxn[0][side_length**2-side_length:side_length**2],cube_nxn[3][0::side_length],cube_nxn[5][0:side_length]
			cube_nxn[0][side_length**2-side_length:side_length**2],cube_nxn[3][0::side_length],cube_nxn[5][0:side_length],cube_nxn[1][side_length-1::side_length] = cube_nxn[1][side_length-1::side_length],cube_nxn[0][side_length**2-side_length:side_length**2],cube_nxn[3][0::side_length],cube_nxn[5][0:side_length]
			rotate_face(2)
			rotate_face(2)
			rotate_face(2)
			cube_nxn[3][0::side_length] = list(reversed(cube_nxn[3][0::side_length]))
			cube_nxn[1][side_length-1::side_length] = list(reversed(cube_nxn[1][side_length-1::side_length]))

		elif turn == "B'":
			cube_nxn[0][0:side_length],cube_nxn[3][side_length-1::side_length],cube_nxn[5][side_length**2-side_length:side_length**2],cube_nxn[1][0::side_length] = cube_nxn[1][0::side_length],cube_nxn[0][0:side_length],cube_nxn[3][side_length-1::side_length],cube_nxn[5][side_length**2-side_length:side_length**2]
			rotate_face(4)
			rotate_face(4)
			rotate_face(4)
			cube_nxn[0][0:side_length] = list(reversed(cube_nxn[0][0:side_length]))
			cube_nxn[5][side_length**2-side_length:side_length**2] = list(reversed(cube_nxn[5][side_length**2-side_length:side_length**2]))
		elif turn == "B2":
			cube_nxn[0][0:side_length],cube_nxn[3][side_length-1::side_length],cube_nxn[5][side_length**2-side_length:side_length**2],cube_nxn[1][0::side_length] = cube_nxn[1][0::side_length],cube_nxn[0][0:side_length],cube_nxn[3][side_length-1::side_length],cube_nxn[5][side_length**2-side_length:side_length**2]
			cube_nxn[0][0:side_length],cube_nxn[3][side_length-1::side_length],cube_nxn[5][side_length**2-side_length:side_length**2],cube_nxn[1][0::side_length] = cube_nxn[1][0::side_length],cube_nxn[0][0:side_length],cube_nxn[3][side_length-1::side_length],cube_nxn[5][side_length**2-side_length:side_length**2]
			rotate_face(4)
			rotate_face(4)
			cube_nxn[0][0:side_length] = list(reversed(cube_nxn[0][0:side_length]))
			cube_nxn[3][side_length-1::side_length] = list(reversed(cube_nxn[3][side_length-1::side_length]))
			cube_nxn[5][side_length**2-side_length:side_length**2] = list(reversed(cube_nxn[5][side_length**2-side_length:side_length**2]))
			cube_nxn[1][0::side_length] = list(reversed(cube_nxn[1][0::side_length]))
		elif turn == "B":
			cube_nxn[0][0:side_length],cube_nxn[3][side_length-1::side_length],cube_nxn[5][side_length**2-side_length:side_length**2],cube_nxn[1][0::side_length] = cube_nxn[1][0::side_length],cube_nxn[0][0:side_length],cube_nxn[3][side_length-1::side_length],cube_nxn[5][side_length**2-side_length:side_length**2]
			cube_nxn[0][0:side_length],cube_nxn[3][side_length-1::side_length],cube_nxn[5][side_length**2-side_length:side_length**2],cube_nxn[1][0::side_length] = cube_nxn[1][0::side_length],cube_nxn[0][0:side_length],cube_nxn[3][side_length-1::side_length],cube_nxn[5][side_length**2-side_length:side_length**2]
			cube_nxn[0][0:side_length],cube_nxn[3][side_length-1::side_length],cube_nxn[5][side_length**2-side_length:side_length**2],cube_nxn[1][0::side_length] = cube_nxn[1][0::side_length],cube_nxn[0][0:side_length],cube_nxn[3][side_length-1::side_length],cube_nxn[5][side_length**2-side_length:side_length**2]
			rotate_face(4)
			cube_nxn[3][side_length-1::side_length] = list(reversed(cube_nxn[3][side_length-1::side_length]))
			cube_nxn[1][0::side_length] = list(reversed(cube_nxn[1][0::side_length]))
		elif turn == "R":
			cube_nxn[0][side_length-1::side_length],cube_nxn[2][side_length-1::side_length],cube_nxn[4][0::side_length],cube_nxn[5][side_length-1::side_length] = cube_nxn[2][side_length-1::side_length],cube_nxn[5][side_length-1::side_length],cube_nxn[0][side_length-1::side_length],cube_nxn[4][0::side_length]
			rotate_face(3)
			cube_nxn[5][side_length-1::side_length] = list(reversed(cube_nxn[5][side_length-1::side_length]))
			cube_nxn[4][0::side_length] = list(reversed(cube_nxn[4][0::side_length]))
		elif turn == "R2":
			cube_nxn[0][side_length-1::side_length],cube_nxn[2][side_length-1::side_length],cube_nxn[4][0::side_length],cube_nxn[5][side_length-1::side_length] = cube_nxn[5][side_length-1::side_length],cube_nxn[4][0::side_length],cube_nxn[2][side_length-1::side_length],cube_nxn[0][side_length-1::side_length]
			rotate_face(3)
			rotate_face(3)
			cube_nxn[4][0::side_length] = list(reversed(cube_nxn[4][0::side_length]))
			cube_nxn[2][side_length-1::side_length] = list(reversed(cube_nxn[2][side_length-1::side_length]))
		elif turn == "R'":
			cube_nxn[0][side_length-1::side_length],cube_nxn[2][side_length-1::side_length],cube_nxn[5][side_length-1::side_length],cube_nxn[4][0::side_length] = cube_nxn[4][0::side_length],cube_nxn[0][side_length-1::side_length],cube_nxn[2][side_length-1::side_length],cube_nxn[5][side_length-1::side_length]
			rotate_face(3)
			rotate_face(3)
			rotate_face(3)
			cube_nxn[0][side_length-1::side_length] = list(reversed(cube_nxn[0][side_length-1::side_length]))
			cube_nxn[4][0::side_length] = list(reversed(cube_nxn[4][0::side_length]))
		elif turn == "L'":
			cube_nxn[0][0::side_length],cube_nxn[2][0::side_length],cube_nxn[4][side_length-1::side_length],cube_nxn[5][0::side_length]	= cube_nxn[2][0::side_length],cube_nxn[5][0::side_length],cube_nxn[0][0::side_length],cube_nxn[4][side_length-1::side_length]
			rotate_face(1)
			rotate_face(1)
			rotate_face(1)
			cube_nxn[5][0::side_length] = list(reversed(cube_nxn[5][0::side_length]))
			cube_nxn[4][side_length-1::side_length] = list(reversed(cube_nxn[4][side_length-1::side_length]))
		elif turn == "L2":
			cube_nxn[0][0::side_length],cube_nxn[2][0::side_length],cube_nxn[4][side_length-1::side_length],cube_nxn[5][0::side_length] = cube_nxn[5][0::side_length],cube_nxn[4][side_length-1::side_length],cube_nxn[2][0::side_length],cube_nxn[0][0::side_length]
			rotate_face(1)
			rotate_face(1)
			cube_nxn[2][0::side_length] = list(reversed(cube_nxn[2][0::side_length]))
			cube_nxn[4][side_length-1::side_length] = list(reversed(cube_nxn[4][side_length-1::side_length]))
		elif turn == "L":
			cube_nxn[0][0::side_length],cube_nxn[2][0::side_length],cube_nxn[4][side_length-1::side_length],cube_nxn[5][0::side_length]	= cube_nxn[4][side_length-1::side_length],cube_nxn[0][0::side_length],cube_nxn[5][0::side_length],cube_nxn[2][0::side_length]
			rotate_face(1)
			cube_nxn[0][0::side_length] = list(reversed(cube_nxn[0][0::side_length]))
			cube_nxn[4][side_length-1::side_length] = list(reversed(cube_nxn[4][side_length-1::side_length]))
		elif turn == "E":
			do_move(1,5,side_length,side_length*side_length-side_length)
			do_move(1,5,side_length,side_length*side_length-side_length)
			do_move(1,5,side_length,side_length*side_length-side_length)
		elif turn == "E2":
			do_move(1,5,side_length,side_length*side_length-side_length)
			do_move(1,5,side_length,side_length*side_length-side_length)
		elif turn == "E'":
			do_move(1,5,side_length,side_length*side_length-side_length)
		elif turn == "y":
			#Why not   cube_nxn[1],cube_nxn[2],cube_nxn[3],cube_nxn[4] = cube_nxn[2],cube_nxn[3],cube_nxn[4],cube_nxn[1] | rotate_face(0) | rotate_face(5)   ?
			do("E'",show=False)
			do("U",show=False)
			do("D'",show=False)
		elif turn == "x":
			do("R",show=False)
			do("L'",show=False)
			for i in r_mid:
				do(i,show=False)
		elif turn == "z":
			do("F",show=False)
			do("B'",show=False)
			for i in f_mid:
				do(i,show=False)
		else: ################################################################# U ######################################################### !!!!!!!!!!!!!!!!!!!!!!!!!!!!
				try:
					x = turn.split("U")
					if len(x) == 1:
						raise IndexError
					do_move((int(x[0])-1)*side_length,int(x[0])*side_length,1)
					if x[1] == "'":
						do_move((int(x[0])-1)*side_length,int(x[0])*side_length,2)
					elif x[1] == "2":
						do_move((int(x[0])-1)*side_length,int(x[0])*side_length,1)
				except IndexError:
					try: ################################################################# F #########################################################
						
						y = turn.split("F")
						if len(y) == 1:
							raise IndexError
						x = int(y[0])
						if y[1] == "'":
							e=cube_nxn[3][x-1::side_length]
							f=cube_nxn[5][side_length*(x-1):side_length*x]
							g=cube_nxn[1][x-2::side_length]
							h=cube_nxn[0][side_length*(x-2):side_length*(x-1)]
							############
							cube_nxn[0][side_length*(x-2):side_length*(x-1)]=e
							cube_nxn[3][x-1::side_length]=reverse_str(f)
							cube_nxn[5][side_length*(x-1):side_length*x]=g
							cube_nxn[1][x-2::side_length]=reverse_str(h)
						elif y[1] == "":
							e=cube_nxn[3][x-1::side_length]
							f=cube_nxn[5][side_length*(x-1):side_length*x]
							g=cube_nxn[1][x-2::side_length]
							h=cube_nxn[0][side_length*(x-2):side_length*(x-1)]
							############
							cube_nxn[0][side_length*(x-2):side_length*(x-1)]=reverse_str(g)
							cube_nxn[3][x-1::side_length]=h
							cube_nxn[5][side_length*(x-1):side_length*x]=reverse_str(e)
							cube_nxn[1][x-2::side_length]=f
						else:
							e=cube_nxn[3][x-1::side_length]
							f=cube_nxn[5][side_length*(x-1):side_length*x]
							g=cube_nxn[1][x-2::side_length]
							h=cube_nxn[0][side_length*(x-2):side_length*(x-1)]
							############
							cube_nxn[0][side_length*(x-2):side_length*(x-1)]=reverse_str(f)
							cube_nxn[3][x-1::side_length]=reverse_str(g)
							cube_nxn[5][side_length*(x-1):side_length*x]=reverse_str(h)
							cube_nxn[1][x-2::side_length]=reverse_str(e)
					except IndexError:
						y = turn.split("L") ################################################################# L #########################################################
						x = int(y[0])
						if y[1] == "'":
							# reversed - a,c | a,b | b,c | a,d | b,d | c,d
							a=cube_nxn[2][x-1::side_length]
							b=cube_nxn[5][x-1::side_length]
							c=cube_nxn[4][side_length-x::side_length]
							d=cube_nxn[0][x-1::side_length]
							cube_nxn[0][x-1::side_length]=a
							cube_nxn[2][x-1::side_length]=b
							cube_nxn[5][x-1::side_length]=reverse_str(c)
							cube_nxn[4][side_length-x::side_length]=reverse_str(d)
						elif y[1] == "":
							# reversed - a,b | a,c | a,d | b,c |              c,d | 
							def r(i):
								return list(reversed(i))
							a=cube_nxn[2][x-1::side_length]
							b=cube_nxn[5][x-1::side_length]
							c=cube_nxn[4][side_length-x::side_length]
							d=cube_nxn[0][x-1::side_length]
							cube_nxn[0][x-1::side_length]=reverse_str(c)
							cube_nxn[2][x-1::side_length]=d
							cube_nxn[5][x-1::side_length]=a
							cube_nxn[4][side_length-x::side_length]=reverse_str(b)
						else:
							# reversed - b,a | 
							a=cube_nxn[2][x-1::side_length]
							b=cube_nxn[5][x-1::side_length]
							c=cube_nxn[4][side_length-x::side_length]
							d=cube_nxn[0][x-1::side_length]
							cube_nxn[0][x-1::side_length]=reverse_str(b)
							cube_nxn[2][x-1::side_length]=reverse_str(c)
							cube_nxn[5][x-1::side_length]=reverse_str(d)
							cube_nxn[4][side_length-x::side_length]=reverse_str(a)
		if show:
			show_cube() # Otočení R,L,F,B
	def quit():
		global visualization,buttons_root
		visualization.destroy()
		buttons_root.destroy()
		global root
		root.destroy() # Vypnout program při kliknutí na křížek
	def show_cube():
		global logo,logo_sticker,side_length
		from PIL import ImageTk,Image
		logo = ImageTk.PhotoImage(Image.open(logo_sticker).resize((30, 35), Image.ANTIALIAS))
		for i in visualization.winfo_children():
			i.destroy()
		ind = 0
		for ia in range(1,side_length+1):
			for ib in range(side_length+1,side_length*2+1):
				a = LabelFrame(visualization,bd=5)
				a.grid(row=ia,column=ib)
				if cube_nxn[0][ind] == "Cyan":
					b = Label(a,image=logo,padx=15,pady=10,bd=5)
				else:
					b = Label(a,bg=cube_nxn[0][ind].lower(),padx=15,pady=10,bd=5)
				b.grid()
				ind+=1
		ind = 0
		for ia in range(side_length+1,side_length*2+1):
			for ib in range(1,side_length+1):
				a = LabelFrame(visualization,bd=5)
				a.grid(row=ia,column=ib)
				if cube_nxn[1][ind] == "Cyan":
					b = Label(a,image=logo,padx=15,pady=10,bd=5)
				else:
					b = Label(a,bg=cube_nxn[1][ind].lower(),padx=15,pady=10,bd=5)
				b.grid()
				ind+=1
		ind = 0
		for ia in range(side_length*2+1,side_length*3+1):
			for ib in range(side_length+1,side_length*2+1):
				a = LabelFrame(visualization,bd=5)
				a.grid(row=ia,column=ib)
				if cube_nxn[5][ind] == "Cyan":
					b = Label(a,image=logo,padx=15,pady=10,bd=5)
				else:
					b = Label(a,bg=cube_nxn[5][ind].lower(),padx=15,pady=10,bd=5)
				b.grid()
				ind+=1
		ind = 0
		for ia in range(side_length+1,side_length*2+1):
			for ib in range(side_length+1,side_length*2+1):
				a = LabelFrame(visualization,bd=5)
				a.grid(row=ia,column=ib)
				if cube_nxn[2][ind] == "Cyan":
					b = Label(a,image=logo,padx=15,pady=10,bd=5)
				else:
					b = Label(a,bg=cube_nxn[2][ind].lower(),padx=15,pady=10,bd=5)
				b.grid()
				ind+=1
		ind = 0
		for ia in range(side_length+1,side_length*2+1):
			for ib in range(side_length*2+1,side_length*3+1):
				a = LabelFrame(visualization,bd=5)
				a.grid(row=ia,column=ib)
				if cube_nxn[3][ind] == "Cyan":
					b = Label(a,image=logo,padx=15,pady=10,bd=5)
				else:
					b = Label(a,bg=cube_nxn[3][ind].lower(),padx=15,pady=10,bd=5)
				b.grid()
				ind+=1
		ind = 0
		for ia in range(side_length+1,side_length*2+1):
			for ib in range(side_length*3+1,side_length*4+1):
				a = LabelFrame(visualization,bd=5)
				a.grid(row=ia,column=ib)
				if cube_nxn[4][ind] == "Cyan":
					b = Label(a,image=logo,padx=15,pady=10,bd=5)
				else:
					b = Label(a,bg=cube_nxn[4][ind].lower(),padx=15,pady=10,bd=5)
				b.grid()
				ind+=1 # Zobrazit kostku
	def undo(move):
		global moves_done,undone_moves
		try:
			last_move=moves_done[-1]
			do(last_move)
			do(last_move)
			do(last_move)
			del moves_done[-1]
			undone_moves.append(last_move)
		except:pass # Tlačítka - undo
	def redo(move):
		global moves_done,undone_moves
		try:
			last_move=undone_moves[-1]
			do(last_move)
			del undone_moves[-1]
			moves_done.append(last_move)
		except:pass# Tlačítka - redo
	def rndsc():
		global turns
		scramble=[]
		scramble.append(random.choice(turns))
		for i in range(0,random.randint(side_length*10-side_length,side_length*10)):
			while True:
				temp = random.choice(turns)
				if temp[0] != scramble[-1][0]:
					scramble.append(temp)
					break
		print(scramble)
		for i in scramble:
			do(i,show=0)
		show_cube()# Tlačítka - zamíchání kostky
	def buttons_gui(): # Panel tlačítek
		global buttons_root,side_length,mod_scramble
		turns_buttons=deepcopy(turns) # Srovnání délky tlačítek
		max_len=len(str(max(turns_buttons,key=len)))
		for x in range(len(turns_buttons)):
			turn_len=len(turns_buttons[x])
			if turn_len!=max_len:
				turns_buttons[x]=turns_buttons[x]+" "*(max_len-turn_len)
		buttons_root = Toplevel() # Config tlačítkového panelu
		buttons_root.title("These Moves Can Be Applied:")
		buttons_root.iconbitmap("rubiks_cube_icon.ico")
		buttons_root.protocol("WM_DELETE_WINDOW",quit)
		buttons = LabelFrame(buttons_root,bd=10)
		buttons.grid()
		ind = 0
		rw = 1
		for txt,i in zip(turns_buttons,turns): # Zobrazení tlačítek
			btn = Button(buttons,text=txt,command=lambda var=i: button_function(var))
			btn.grid(row=rw,column=ind)
			ind+=1
			if ind == 20:
				ind = 0
				rw+=1

		reset_the_cube_button = Button(buttons,text="Reset",command=reset_the_cube).grid(row=rw+1,column=0,columnspan=2) # Zobrazení etc tlačítek
		solve_the_cube_button = Button(buttons,text="Solve",command=solve_the_cube).grid(row=rw+1,column=2,columnspan=2)
		undo_button = Button(buttons,text="Undo ",command=lambda var=txt: undo(var)).grid(row=rw+1,column=4,columnspan=2)
		redo_button = Button(buttons,text="Redo ",command=lambda var=txt: redo(var)).grid(row=rw+1,column=6,columnspan=2)
		random_scramble_button = Button(buttons,text="RNDSC",command=rndsc).grid(row=rw+1,column=8,columnspan=2)
		quit_button = Button(buttons,text="Quit ",command=quit).grid(row=rw+1,column=10,columnspan=2)
	solve_the_cube(show=False)
	buttons_gui()
	visualization = Toplevel()
	visualization.iconbitmap("rubiks_cube_icon.ico")
	visualization.protocol("WM_DELETE_WINDOW",quit)
	visualization.title(" ".join(input_scramble))
	#s_t0 = time.time()
	for i in scramble:	
		do(i)
	show_cube()
"""