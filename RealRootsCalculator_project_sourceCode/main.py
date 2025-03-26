from tkinter import *
from tkinter import messagebox
from sympy import *
from PIL import Image, ImageTk, ImageDraw
import re
import threading  # لضمان عداد الوقت بدون تجميد الواجهة
import matplotlib.pyplot as plt
import numpy as np


#Important!!!!!!!
#You must put the resources folder to make the main.py file run correctly!


#########################################################################################
############################################--create the main window--###################
#########################################################################################
realRootsCalc_project = Tk()
realRootsCalc_project.geometry('900x630+240+50')
realRootsCalc_project.title('Real Roots Calculator')
realRootsCalc_project.iconbitmap(r'resources/Icon.ico')
realRootsCalc_project.resizable(False,False)
realRootsCalc_project.withdraw()
#########################################################################################








#########################################################################################
#########################################--Functions--###################################
#########################################################################################
def format_equation(equation_str):
    return equation_str.replace("^", "**")

#########################################################################################

def find_real_roots(equation_str):
    try:
        equation_str = format_equation(equation_str)
        equation_str = convert_expression(equation_str)
        x = symbols('x')
        equation = sympify(equation_str)

        # استخدام real_roots للحصول على الجذور الدقيقة
        roots = real_roots(equation)

        # تحويل الجذور إلى قيم تقريبية
        real_roots_approx = [round(float(N(r)), 3) for r in roots]

        result_label.config(fg='green', font=('Inter', 15, 'bold'))
        result_label.place(x=565, y=270)

        if real_roots_approx:
            return real_roots_approx, equation
        else:
            return "No real roots found.", None

    except Exception as e:
        result_label.config(fg='red', font=('Inter', 12), wraplength=295)
        result_label.place(x=550, y=230)
        return (f"Invalid equation: {e}"), None

#########################################################################################

def calculate_error_rate(equation, x, approx_roots):
    try:
        """ حساب معدل الخطأ بالتعويض في المعادلة، وإظهاره كنسبة مئوية """
        error_rates = [round(float(N(abs(equation.subs(x, approx)) * 100)), 3) for approx in approx_roots]
        error_label.config(fg='green', font=('Inter', 15, 'bold'))
        return error_rates
    except Exception as e:
        error_label.config(fg='red', wraplength=250)
        return f"Invalid equation: {e}"

#########################################################################################

def convert_expression(expression):
    # تحويل أي رقم يتبعه حرف إلى رقم * حرف
    converted_expression = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expression)
    return converted_expression

#########################################################################################

# دالة لحساب الجذور الحقيقية
def find_real_roots_2(equation_str):
    x = symbols('x')
    try:
        equation = sympify(equation_str)
        roots = real_roots(equation)
        real_roots_approx = [round(float(N(r)), 3) for r in roots]

        num_roots = len(real_roots_approx)
        roots_str = ", ".join(map(str, real_roots_approx))

        return num_roots, real_roots_approx, equation
    except Exception as e:
        return 0, [], None

#########################################################################################

# دالة رسم المعادلة
def plot_equation(equation_str):
    try:
        equation_str = format_equation(equation_str)
        equation_str = convert_expression(equation_str)
        x = symbols('x')
        equation = sympify(equation_str)

        # توليد نقاط الرسم
        x_vals = np.linspace(-10, 10, 1000)
        y_vals = [float(equation.subs(x, val)) for val in x_vals]

        # حساب الجذور والمعلومات
        num_roots, roots, equation_obj = find_real_roots_2(equation_str)

        # فتح نافذة الرسم
        plt.figure("Graph of equations")
        plt.plot(x_vals, y_vals, label=f'y = {equation}')

        # تمييز الجذور على الرسم
        for root in roots:
            plt.scatter(root, 0, color='red', zorder=5)
            plt.annotate(f"{root}", (root, 0), textcoords="offset points", xytext=(5, 5))

        # تحديد المحاور والشبكة
        plt.axhline(0, color='black', linewidth=1)
        plt.axvline(0, color='black', linewidth=1)
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.legend()

        # عرض معلومات إضافية
        info_text = f"Number of real roots: {num_roots}\n"
        if num_roots > 0:
            info_text += f"The roots: {', '.join(map(str, roots))}"

        plt.title(info_text)
        plt.show()

    except Exception as e:
        messagebox.showerror("Error", f"An error accurred while graphing the equation: {e}")


#########################################################################################



# دالة لتحريك صورة الـ GIF
def animate_gif(label, gif, frame=0):
    try:
        # تحديث الصورة بإطار جديد في كل مرة
        gif.seek(frame)
        frame_image = ImageTk.PhotoImage(gif)
        label.config(image=frame_image)
        label.image = frame_image

        # الانتقال إلى الإطار التالي بعد 100 مللي ثانية (سرعة الحركة)
        label.after(20, animate_gif, label, gif, (frame + 1) % gif.n_frames)
    except Exception:
        pass  # في حالة انتهاء الصورة


#########################################################################################

# دالة لعرض نافذة التحميل
def show_loading_window(root):
    loading_window = Toplevel(root)
    loading_window.overrideredirect(True)
    loading_window.geometry("700x400+350+200")

    # تحميل صورة GIF
    gif = Image.open(r"resources/Loading_logo.gif")  # استبدل "loading.gif" باسم ملفك

    # عرض أول إطار من الصورة
    label = Label(loading_window)
    label.pack(expand=True)

    # بدء حركة الـ GIF
    animate_gif(label, gif)

    # بعد 5 ثوانٍ، يتم إغلاق نافذة التحميل وفتح الرئيسية
    loading_window.after(5000, lambda: open_main_window(root, loading_window))

#########################################################################################

# دالة لفتح النافذة الرئيسية
def open_main_window(root, loading_window):
    loading_window.destroy()  # إغلاق نافذة التحميل
    root.deiconify()  # إظهار النافذة الرئيسية

#########################################################################################

def show_frame(frame):
    frame.tkraise()

frame_home = Frame(realRootsCalc_project,width='900',height='630',bg='black')
frame_page_1 = Frame(realRootsCalc_project,width='900',height='630',bg='black')
frame_home.place(x=0, y=0)
frame_page_1.place(x=0, y=0)

#########################################################################################


# الجزء الخاص بالصورة (تحزير !!! عدم الاقتراب)
# تحميل الصورة ومعالجة الزوايا والخلفية السوداء
def process_image(image_path, size, radius):
    img = Image.open(image_path).resize(size, Image.LANCZOS).convert("RGBA")

    # إنشاء قناع للزوايا الدائرية
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, size[0], size[1]), radius=radius, fill=255)
    img.putalpha(mask)

    # استبدال الخلفية البيضاء بالسوداء
    black_bg = Image.new("RGBA", size, (0, 0, 0, 255))
    final_img = Image.alpha_composite(black_bg, img)

    return final_img

#########################################################################################

def check_nextbutton():
    checked_text = method.cget('text')
    if checked_text.strip() == 'Please select a method':
        messagebox.showerror('Something Wrong', 'Please select a method')
    else:
        show_frame(frame_page_1)

#########################################################################################
def append_text(text):
    if equation_input.get() == "Example: (X³−2X+1)":
        equation_input.delete(0, END)

    equation_input.insert(END, text)


###################################################################################
def buttonback_command():
    method_text.set('Please select a method')
    show_frame(frame_home)


#########################################################################################

# دالة لعرض الجذور
def display_roots():
    try:
        global stored_roots, stored_equation  # تعريف المتغيرات كـ global
        equation_str = equation_input.get()  # قراءة المعادلة من Entry
        roots, equation = find_real_roots(equation_str)  # استدعاء دالة الجذور

        if isinstance(roots, list):
            stored_roots = roots  # تخزين الجذور في متغير عالمي
            stored_equation = equation  # تخزين المعادلة الأصلية
            result_text = f"{roots}"
        else:
            stored_roots = []  # تفريغ الجذور إذا فشلت العملية
            stored_equation = None
            result_text = roots  # في حالة وجود رسالة خطأ

        result_label.config(text=result_text)  # تحديث نص الـ Label
    except Exception as e:
        result_label.place(x=560, y=236)
        result_label.config(fg='red', wraplength=250, text=f"SomeThing wrong: {e}")
#########################################################################################
# دالة لعرض نسبة الخطأ
def display_error_rate():
    try:
        if stored_roots and stored_equation:  # تأكد إن الجذور والمعادلة محفوظين
            errors = calculate_error_rate(stored_equation, symbols('x'), stored_roots)
            error_label.config(fg='green', font=('Inter', 14, 'bold'))
            error_label.place(x=577, y=415)
            error_label.config(text=f"%{errors}")
        else:
            error_label.config(fg='orange')
            result_text = "You have to calculate the Roots first."
            error_label.config(fg='red', font=('Inter', 13, 'bold'),wraplength=250)
            error_label.place(x=577, y=408)
            error_label.config(text=result_text)
    except Exception as e:
        error_label.config(fg='red', font=('Inter', 13, 'bold'), wraplength=250)
        error_label.place(x=555, y=410)
        error_label.config(fg='red', wraplength=250, text=f"SomeThing wrong: {e}")

#########################################################################################
########################################--componants of the first page (Home_page)--#####
#########################################################################################

# تحديد أبعاد الصورة والمسافات
image_path = r'resources/homePIC.png'
img_width, img_height = 370, 600  # ضبط الارتفاع ليكون متناسقًا مع النافذة
img = process_image(image_path, (img_width, img_height), radius=8)  # تقليل التدوير إلى 8 بيكسل
photo = ImageTk.PhotoImage(img)

# تحديد المسافات بحيث تكون العلوية والسفلية متساوية
padding_side = 10  # مسافة الجوانب اليسرى واليمنى
padding_top_bottom = (630 - img_height) // 2  # حساب التساوي بين الأعلى والأسفل
frame_x = 900 - img_width - padding_side
frame_y = padding_top_bottom  # توسيط الصورة بشكل مثالي

# إنشاء Frame جديد للصورة
image_frame = Frame(frame_home, width=img_width, height=img_height, bg='black')
image_frame.place(x=frame_x, y=frame_y)

# وضع الصورة داخل الـ Frame
image_label = Label(image_frame, image=photo, borderwidth=0, bg='black')
image_label.pack()
#########################################################################################


button_font = ("Arial", 14, "bold")  # تكبير الخط داخل الأزرار
main_button_font = ("Arial", 16, "bold")

###################################################################################
newtonRaphsonBUTTON_image = PhotoImage(file=r'resources/newtonRaphsonBUTTON.png')
newtonRaphsonBUTTON_image = newtonRaphsonBUTTON_image.subsample(2,2)
newtonRaphsonBUTTON = Button(frame_home, border=0, image = newtonRaphsonBUTTON_image, bg='black', activebackground='black', cursor='hand2', command=lambda : method_text.set('->Newton-Raphson Method<-'))
newtonRaphsonBUTTON.place(x=40,y=200)


###################################################################################
falsePositionBUTTON_image = PhotoImage(file=r'resources/falsePositionBUTTON.png')
falsePositionBUTTON_image = falsePositionBUTTON_image.subsample(2,2)
falsePositionBUTTON = Button(frame_home, border=0, image = falsePositionBUTTON_image, bg='black', activebackground='black', cursor='hand2', command=lambda : method_text.set('->False Position Method<-'))
falsePositionBUTTON.place(x=40,y=250)

###################################################################################
secantBUTTON_image = PhotoImage(file=r'resources/secantBUTTON.png')
secantBUTTON_image = secantBUTTON_image.subsample(2,2)
secantBUTTON = Button(frame_home, border=0, image = secantBUTTON_image, bg='black', activebackground='black', cursor='hand2', command=lambda : method_text.set('->Secant Method<-'))
secantBUTTON.place(x=40,y=300)

###################################################################################
bisectionBUTTON_image = PhotoImage(file=r'resources/bisectionBUTTON.png')
bisectionBUTTON_image = bisectionBUTTON_image.subsample(2,2)
bisectionBUTTON = Button(frame_home, border=0, image = bisectionBUTTON_image, bg='black', activebackground='black', cursor='hand2', command=lambda : method_text.set('->Bisection Method<-'))
bisectionBUTTON.place(x=40,y=350)

###################################################################################

###################################################################################
nextBUTTON_image = PhotoImage(file=r'resources/nextBUTTON.png')
nextBUTTON_image = nextBUTTON_image.subsample(2,2)
nextBUTTON = Button(frame_home, border=0, image = nextBUTTON_image, bg='black', activebackground='black', cursor='hand2', command=check_nextbutton)
nextBUTTON.place(x=45,y=490)
realRootsCalc_project.bind('<Return>', lambda event: check_nextbutton())
######################################################
#العناوين

word_button_font = ("Arial",11, "normal")
woord_button_font = ("Arial",30, "bold")
wooord_button_font = ("Arial",17, "normal")



RealROOTSCalculator = Label(frame_home,text='Real Roots calculator',fg='#B5B3AA',bg='black',font=woord_button_font)
RealROOTSCalculator.place(x=20,y=40)

method_text = StringVar()
method_text.set('Please select a method')
method = Label(frame_home,textvariable=method_text,fg='#7487B0',bg='black',font=wooord_button_font)
method.place(x=40,y=150)

COPYr = Label(frame_home,text='@made by {code<X>pert}',fg='cyan',bg='black',font=word_button_font )
COPYr.place(x=40,y=600)






#########################################################################################
#######################################--componants of the second page (page_2)--########
#########################################################################################
back_ground = PhotoImage(file=r'resources/Back_ground.png')
back_ground_show = Label(frame_page_1, image=back_ground)
back_ground_show.place(x=-180, y=-290)
#########################################################################################
RealRootsCalculator_Label = Label(frame_page_1, text="Real Roots Calculator", fg='#B5B3AA', font=('Inter', 30, 'bold'),bg='#343331')
RealRootsCalculator_Label.place(x=35, y=25)
#########################################################################################
equation_input = Entry(frame_page_1, bg=r'#9B9B99', fg=r'#FFFFFF', font=('Segoe UI', 14), highlightthickness=1, highlightbackground='#343331', highlightcolor='#4F628A', selectbackground='#526590')
equation_input.insert(0, "Example: (X³−2X+1)")
equation_input.place(x=35, y=150, width=340, height=110)
equation_input.bind('<Button-1>', lambda event: equation_input.delete(0, END) if equation_input.get() == "Example: (X³−2X+1)" else None)
###################################################################################
enterYourEquation_Label = Label(frame_page_1, text="Enter your equation ", fg='#7487B0', font=('Inter', 13),bg='#343331')
enterYourEquation_Label.place(x=35, y=125)
###################################################################################

###################################################################################
buttonPLUS_image = PhotoImage(file=r'resources/buttonPLUS.png')
buttonPLUS_image = buttonPLUS_image.subsample(2,2)
buttonPLUS = Button(frame_page_1, border=0, image=buttonPLUS_image, bg='#343331', activebackground='#343331', cursor='hand2', command= lambda : append_text('+'))
buttonPLUS.place(x=35,y=280)
###################################################################################
buttonSUB_image = PhotoImage(file=r'resources/buttonSUB.png')
buttonSUB_image = buttonSUB_image.subsample(2,2)
buttonSUB = Button(frame_page_1, border=0, image=buttonSUB_image, bg='#343331', activebackground='#343331', cursor='hand2', command= lambda : append_text('-'))
buttonSUB.place(x=91,y=280)
###################################################################################
buttonMULTIPLI_image = PhotoImage(file=r'resources/buttonMULTIPLI.png')
buttonMULTIPLI_image = buttonMULTIPLI_image.subsample(2,2)
buttonMULTIPLI = Button(frame_page_1, border=0, image=buttonMULTIPLI_image, bg='#343331', activebackground='#343331', cursor='hand2', command= lambda : append_text('*'))
buttonMULTIPLI.place(x=148,y=280)
###################################################################################
buttonROOT_image = PhotoImage(file=r'resources/buttonROOT.png')
buttonROOT_image = buttonROOT_image.subsample(2,2)
buttonROOT = Button(frame_page_1, border=0, image=buttonROOT_image, bg='#343331', activebackground='#343331', cursor='hand2', command= lambda : append_text('sqrt(x)'))
buttonROOT.place(x=35,y=330)
###################################################################################
buttonROOTTH_image = PhotoImage(file=r'resources/buttonROOTTH.png')
buttonROOTTH_image = buttonROOTTH_image.subsample(2,2)
buttonROOTTH = Button(frame_page_1, border=0, image=buttonROOTTH_image, bg='#343331', activebackground='#343331', cursor='hand2', command= lambda : append_text('root(x,3)'))
buttonROOTTH.place(x=91,y=330)
###################################################################################
buttonLOG_image = PhotoImage(file=r'resources/buttonLOG.png')
buttonLOG_image = buttonLOG_image.subsample(2,2)
buttonLOG = Button(frame_page_1, border=0, image=buttonLOG_image, bg='#343331', activebackground='#343331', cursor='hand2', command= lambda : append_text('log(x,10)'))
buttonLOG.place(x=148,y=330)
###################################################################################
buttonSIN_image = PhotoImage(file=r'resources/buttonSIN.png')
buttonSIN_image = buttonSIN_image.subsample(2,2)
buttonSIN = Button(frame_page_1, border=0, image=buttonSIN_image, bg='#343331', activebackground='#343331', cursor='hand2', command= lambda : append_text('sin(x)'))
buttonSIN.place(x=35,y=380)
###################################################################################
buttonCOS_image = PhotoImage(file=r'resources/buttonCOS.png')
buttonCOS_image = buttonCOS_image.subsample(2,2)
buttonCOS = Button(frame_page_1, border=0, image=buttonCOS_image, bg='#343331', activebackground='#343331', cursor='hand2', command= lambda : append_text('cos(x)'))
buttonCOS.place(x=91,y=380)
###################################################################################
buttonTAN_image = PhotoImage(file=r'resources/buttonTAN.png')
buttonTAN_image = buttonTAN_image.subsample(2,2)
buttonTAN = Button(frame_page_1, border=0, image=buttonTAN_image, bg='#343331', activebackground='#343331', cursor='hand2', command= lambda : append_text('tan(x)'))
buttonTAN.place(x=148,y=380)
###################################################################################
buttonDIVISION_image = PhotoImage(file=r'resources/buttonDIVISION.png')
buttonDIVISION_image = buttonDIVISION_image.subsample(2,2)
buttonDIVISION = Button(frame_page_1, border=0, image=buttonDIVISION_image, bg='#08090B', activebackground='#08090B', cursor='hand2', command= lambda : append_text('/'))
buttonDIVISION.place(x=220,y=280)
###################################################################################
buttonLN_image = PhotoImage(file=r'resources/buttonLN.png')
buttonLN_image = buttonLN_image.subsample(2,2)
buttonLN = Button(frame_page_1, border=0, image=buttonLN_image, bg='#08090B', activebackground='#08090B', cursor='hand2', command= lambda : append_text('log(x,E)'))
buttonLN.place(x=220,y=330)
###################################################################################
buttonCOT_image = PhotoImage(file=r'resources/buttonCOT.png')
buttonCOT_image = buttonCOT_image.subsample(2,2)
buttonCOT = Button(frame_page_1, border=0, image=buttonCOT_image, bg='#343331', activebackground='#343331', cursor='hand2', command= lambda : append_text('1/tan(x)'))
buttonCOT.place(x=220,y=380)
###################################################################################
buttonEXPONENT_image = PhotoImage(file=r'resources/buttonEXPONENT.png')
buttonEXPONENT_image = buttonEXPONENT_image.subsample(2,2)
buttonEXPONENT = Button(frame_page_1, border=0, image=buttonEXPONENT_image, bg='#08090B', activebackground='#08090B', cursor='hand2', command= lambda : append_text('x^'))
buttonEXPONENT.place(x=276,y=280)
###################################################################################
buttonE_image = PhotoImage(file=r'resources/buttonE.png')
buttonE_image = buttonE_image.subsample(2,2)
buttonE = Button(frame_page_1, border=0, image=buttonE_image, bg='#08090B', activebackground='#08090B', cursor='hand2', command= lambda : append_text('exp(x)'))
buttonE.place(x=276,y=330)
###################################################################################
buttonSEC_image = PhotoImage(file=r'resources/buttonSEC.png')
buttonSEC_image = buttonSEC_image.subsample(2,2)
buttonSEC = Button(frame_page_1, border=0, image=buttonSEC_image, bg='#343331', activebackground='#343331', cursor='hand2', command= lambda : append_text('1/cos(x)'))
buttonSEC.place(x=276,y=380)
###################################################################################
buttonXvariable_image = PhotoImage(file=r'resources/buttonXvariable.png')
buttonXvariable_image = buttonXvariable_image.subsample(2,2)
buttonXvariable = Button(frame_page_1, border=0, image=buttonXvariable_image, bg='#08090B', activebackground='#08090B', cursor='hand2', command= lambda : append_text('x'))
buttonXvariable.place(x=332,y=280)
###################################################################################
buttonPI_image = PhotoImage(file=r'resources/buttonPI.png')
buttonPI_image = buttonPI_image.subsample(2,2)
buttonPI = Button(frame_page_1, border=0, image=buttonPI_image, bg='#08090B', activebackground='#08090B', cursor='hand2', command= lambda : append_text('pi'))
buttonPI.place(x=332,y=330)
###################################################################################
buttonCSC_image = PhotoImage(file=r'resources/buttonCSC.png')
buttonCSC_image = buttonCSC_image.subsample(2,2)
buttonCSC = Button(frame_page_1, border=0, image=buttonCSC_image, bg='#343331', activebackground='#343331', cursor='hand2', command= lambda : append_text('1/sin(x)'))
buttonCSC.place(x=332,y=380)

###################################################################################
buttonBACK_image = PhotoImage(file=r'resources/buttonBACK.png')
buttonBACK_image = buttonBACK_image.subsample(2,2)
buttonBACK = Button(frame_page_1, border=0, image=buttonBACK_image, bg='#343331', activebackground='#343331', cursor='hand2', command=buttonback_command)
buttonBACK.place(x=35,y=500)
realRootsCalc_project.bind('<Escape>', lambda event: buttonback_command())
###################################################################################

###################################################################################
buttonRESULT_image = PhotoImage(file=r'resources/buttonRESULT.png')
buttonRESULT_image = buttonRESULT_image.subsample(2,2)
buttonRESULT = Button(frame_page_1, border=0, image=buttonRESULT_image, bg='#343331', activebackground='#343331', cursor='hand2', command=display_roots)
buttonRESULT.place(x=550,y=170)
###################################################################################
reelROOTSoutput_image1 = Image.open(r'resources/reelROOTSoutput.png')
reelROOTSoutput_image2 = reelROOTSoutput_image1.resize((300, 120))
reelROOTSoutput_image3 = ImageTk.PhotoImage(reelROOTSoutput_image2)
reelROOTSoutput = Label(frame_page_1, border=0, image=reelROOTSoutput_image3, bg='#343331', activebackground='#343331', cursor='pirate')
reelROOTSoutput.place(x=551,y=210)
###################################################################################
buttonEROR_image = PhotoImage(file=r'resources/buttonEROR.png')
buttonEROR_image = buttonEROR_image.subsample(2,2)
buttonEROR = Button(frame_page_1, border=0, image=buttonEROR_image, bg='#343331', activebackground='#343331', cursor='hand2', command=display_error_rate)
buttonEROR.place(x=550,y=350)
###################################################################################
ERORoutput_image1 = Image.open(r'resources/ERORoutput.png')
ERORoutput_image2 = ERORoutput_image1.resize((250, 80))
ERORoutput_image3 = ImageTk.PhotoImage(ERORoutput_image2)
ERORoutput = Label(frame_page_1, border=0, image=ERORoutput_image3, bg='#343331', activebackground='#343331', cursor='pirate')
ERORoutput.place(x=551,y=390)
###################################################################################
COPYr = Label(frame_page_1,text='@made by {code<X>pert}',fg='cyan',bg='#343331',font='word_button_font' )
COPYr.place(x=40,y=600)
###################################################################################
result_label = Label(frame_page_1,text='',fg='white',bg='#9B9B99',font=('Inter', 13, 'bold'))
result_label.place(x=560,y=245)
###################################################################################
error_label = Label(frame_page_1,text='',fg='white',bg='#9B9B99',font=('Inter', 13, 'bold'))
error_label.place(x=572,y=405)
###################################################################################
# زر لعرض الرسم البياني
plot_button_image1 = Image.open(r'resources/button_graph-the-equation.png')
plot_button_image2 = plot_button_image1.resize((200,50))
plot_button_image3 = ImageTk.PhotoImage(plot_button_image2)
plot_button = Button(frame_page_1, border=0, image=plot_button_image3, bg='#343331', activebackground='#343331', cursor='hand2', command=lambda: plot_equation(equation_input.get()))
plot_button.place(x=560,y=500)
###################################################################################
###################################################################################
###################################################################################

show_frame(frame_home)
threading.Thread(target=show_loading_window, args=(realRootsCalc_project,), daemon=True).start()
realRootsCalc_project.mainloop()
