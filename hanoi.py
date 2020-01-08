from tkinter import *
from tkinter import messagebox

class Board():
    MOVE_UP=1
    MOVE_LEFT_OR_RIGHT=2
    MOVE_DOWN=3
        
    def move_single_disc(self):
        if self.moving_direction==Board.MOVE_UP:
            self.canvas.move(self.piece_to_move,0,-1)
            self.times-=1
            if self.times<=0:
                self.moving_direction=Board.MOVE_LEFT_OR_RIGHT
                self.diff_x=1 if self.move_to>self.move_from else -1
                left_to=self.left_values[self.move_to]
                left_from=self.left_values[self.move_from]
                self.times=abs(left_to-left_from)
            self.canvas.after(2,self.move_single_disc)
        elif self.moving_direction==Board.MOVE_LEFT_OR_RIGHT:
            self.canvas.move(self.piece_to_move,self.diff_x,0)
            self.times-=1
            if self.times<=0:
                self.moving_direction=Board.MOVE_DOWN
                self.times = self.height - 220 - 20*len(self.rod_discs[self.move_to])
            self.canvas.after(2,self.move_single_disc)
        else:
            self.canvas.move(self.piece_to_move,0,1)
            self.times-=1
            if self.times<=0:
                self.rod_discs[self.move_from].pop()
                self.rod_discs[self.move_to].append(self.piece_to_move)
                self.move_no_mod_3+=1
                if self.move_no_mod_3==3:
                    self.move_no_mod_3=0
                self.canvas.after(2,self.move_discs)
                return
            self.canvas.after(2,self.move_single_disc)
            
    def move_discs(self):
        if len(self.rod_discs[2])<self.no_of_discs:
            cur_move=self.move_order[self.move_no_mod_3]
            rod_1=cur_move[0]
            rod_2=cur_move[1]
            if len(self.rod_discs[rod_1])==0:
                self.move_from=rod_2
                self.move_to=rod_1
                self.piece_to_move=self.rod_discs[rod_2][-1]
                self.coords_to_move=self.canvas.coords(self.piece_to_move)
            elif len(self.rod_discs[rod_2])==0:
                self.move_from=rod_1
                self.move_to=rod_2
                self.piece_to_move=self.rod_discs[rod_1][-1]
                self.coords_to_move=self.canvas.coords(self.piece_to_move)
            else:
                coords1=self.canvas.coords(self.rod_discs[rod_1][-1])
                coords2=self.canvas.coords(self.rod_discs[rod_2][-1])
                if coords1[2]-coords1[0]<coords2[2]-coords2[0]:
                    self.move_from=rod_1
                    self.move_to=rod_2
                    self.piece_to_move=self.rod_discs[rod_1][-1]
                else:
                    self.move_from=rod_2
                    self.move_to=rod_1
                    self.piece_to_move=self.rod_discs[rod_2][-1]
                self.coords_to_move=self.canvas.coords(self.piece_to_move)
            
            # Move up
            top_coords=self.coords_to_move[1]
            bottom_coords=int(self.coords_to_move[3])
            self.piece_to_move
            self.times=bottom_coords-220
            self.moving_direction=Board.MOVE_UP
            self.canvas.after(2,self.move_single_disc)
        else:
            self.entry.config(state='normal')
            self.entry.delete(0,'end')
               
        
    def start(self):
        disc_height=20
        center=self.width*1/6
        self.rod_discs=[[],[],[]]
        self.move_no_mod_3=0
        
        # Remove old discs
        self.canvas.delete('disc')
        
        # Place new discs
        for i in range (0,self.no_of_discs):
            disc_no=self.no_of_discs-i-1
            disc_width=(i+1)*self.width/30
            start_x=center-disc_width/2
            end_x=center+disc_width/2
            start_y=self.height-disc_no*disc_height
            end_y=start_y-disc_height
            rect=self.canvas.create_rectangle(start_x,start_y,end_x,end_y,fill='blue',tags='disc')
            self.rod_discs[0].insert(0,rect)
            
        if self.no_of_discs%2:
            self.move_order=[[0,2],[0,1],[2,1]]
        else:
            self.move_order=[[0,1],[0,2],[1,2]]
            
        move_no_mod_3=0
        self.canvas.after(2,self.move_discs())
        
   
    def handle_event(self,evt):     
        if evt.keysym != 'Return' and evt.keysym!='KP_Enter':
            return
        self.entry.configure(state='disabled')
        try:
            self.no_of_discs=int(self.entry.get())
            if self.no_of_discs<1 or self.no_of_discs>10:
                messagebox.showerror('Error','Please enter an integer (1-10)')
                self.entry.configure(state='normal')
                self.entry.delete(0,'end')
                return
            self.canvas.after(2, self.start)
            
        except ValueError:
            messagebox.showerror('Error','Please enter an integer (1-10)')
            self.entry.configure(state='normal')
            self.entry.delete(0,'end')
            
    def add_rods(self):
        self.left_values=[]
        for i in range(3):
            center=self.width*(1/6+i/3)
            start_x=center-2
            end_x=center+2
            end_y=self.height-220
            a=self.canvas.create_rectangle(start_x, self.height, end_x,end_y,fill='yellow')
            self.left_values.append(self.canvas.bbox(a)[0])
            
    def add_canvas(self,root):
        self.canvas=Canvas(root,background='black', height=self.height,width=self.width)
        self.add_rods()
        self.canvas.pack(side='bottom')
        
    def add_input(self, root):
        label=Label(self.frame,text='Number of discs(1-10): ')
        label.pack(side='left')
        self.entry = Entry(self.frame,text='7')
        self.entry.bind("<KeyRelease>", self.handle_event)
        self.entry.pack(side='left')
        self.frame.pack(side='bottom',anchor='w')
        
    def __init__(self, root):
        self.no_of_discs=0
        self.height=480
        self.width=640
        self.frame = Frame(root,background='blue',width=self.width,padx='5p')
        self.add_canvas(root)
        self.add_input(root)
        

root = Tk()
board=Board(root)
root.mainloop()
