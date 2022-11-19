#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
# @Time: 2022/11/19 5:56 PM
# @Author: Guilian Chen
# @Software: PyCharm
# @Description: Python GUI application —— different classifications can obtain different loans
"""

import tkinter as tk
from tkinter import ttk, END


class LoanCalculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Individual house loan calculation")
        self.window.geometry('800x600')
        frame = tk.Frame(self.window)
        frame.pack(padx=20, pady=20)

        # 定义贷款类型与贷款年限之间的关系
        loanTypeYear = {
            "First time buyer": (10, 20, 30),
            "Returning buyer": (10, 20, 30),
            "Buy-to-Let": (10, 20)  # 注意用于出租的只能贷10年和20年的
        }

        # ------ input ------#
        # Applicant First Name
        tk.Label(frame, justify=tk.LEFT, text="First Name ", ).grid(sticky='w', row=1, column=1, columnspan=3)   # sticky='w' 代表左对齐
        self.firstName = tk.StringVar()
        tk.Entry(frame, width=20, textvariable=self.firstName).grid(row=1, column=4)

        # Applicant Last Name
        tk.Label(frame, justify=tk.LEFT, text="Last Name ", ).grid(sticky='w', row=2, column=1, columnspan=3)
        self.lastName = tk.StringVar()
        tk.Entry(frame, width=20, textvariable=self.lastName).grid(row=2, column=4)

        # Applicant Date of Birth
        tk.Label(frame, justify=tk.LEFT, text="Date of Birth(yyyy/mm/dd) ", ).grid(sticky='w', row=3, column=1, columnspan=3)
        self.dateOfBirth = tk.StringVar()
        tk.Entry(frame, width=20, textvariable=self.dateOfBirth).grid(row=3, column=4)

        # Applicant Income
        tk.Label(frame, justify=tk.LEFT, text="Annual Income(€) ", ).grid(sticky='w', row=4, column=1, columnspan=3)
        self.income = tk.StringVar()
        tk.Entry(frame, width=20, textvariable=self.income).grid(row=4, column=4)

        # Applicant Property cost
        tk.Label(frame, justify=tk.LEFT, text="Property cost ", ).grid(sticky='w', row=5, column=1, columnspan=3)
        self.propertyCost = tk.StringVar()
        tk.Entry(frame, width=20, textvariable=self.propertyCost).grid(row=5, column=4)

        # Applicant Loan Type
        tk.Label(frame, justify=tk.LEFT, text="Loan Type ", ).grid(sticky='w', row=6, column=1, columnspan=3)
        self.loanType = tk.StringVar()
        loanType = ttk.Combobox(frame, width=19, textvariable=self.loanType, state='readonly')
        loanType['values'] = list(loanTypeYear.keys())
        loanType.grid(row=6, column=4)

        # Applicant Loan Term
        tk.Label(frame, justify=tk.LEFT, text="Loan Term(Year) ", ).grid(sticky='w', row=7, column=1, columnspan=3)
        self.loanTerm = tk.StringVar()
        loanYear = ttk.Combobox(frame, width=19, textvariable=self.loanTerm, state='readonly')
        loanYear.grid(row=7, column=4)

        # Loan Term 的下拉框 根据 Loan Type的值进行联动
        def xFunc(event):
            loanYear.delete(0, tk.END)
            value = self.loanType.get()
            loanYear['value'] = loanTypeYear[value]

        loanType.bind("<<ComboboxSelected>>", xFunc)

        # 作为空行，拉开距离
        tk.Frame(frame, height=20).grid(row=8, column=4, columnspan=7)

        # ------ button ------#
        # 按钮，事件监听函数为calculate
        buttonstyle = ttk.Style()
        buttonstyle.configure('my.TButton', font=('Helvetica', 20))
        ttk.Button(frame, width=15, text="Loan review result", command=self.calculate, style="my.TButton").grid(row=9, column=4, columnspan=1, pady=0)

        # ------ output ------#
        # isIncomeSatisfied
        tk.Label(frame, justify=tk.LEFT, text="isIncomeSatisfied ", ).grid(sticky='w', row=10, column=1, columnspan=3)
        self.isIncomeSatisfiedVar = tk.StringVar()
        self.isIncomeSatisfied = tk.Label(frame, height=2, width=40, textvariable=self.isIncomeSatisfiedVar).grid(row=10, column=4)

        # Required Deposit Cash Amount
        tk.Label(frame, justify=tk.LEFT, text="Required Deposit Cash Amount(€) ", ).grid(sticky='w', row=11, column=1, columnspan=3)
        self.requiredCashVar = tk.StringVar()
        tk.Label(frame, height=2, width=20, textvariable=self.requiredCashVar).grid(row=11, column=4)

        # Total Repayment Amount
        tk.Label(frame, justify=tk.LEFT, text="Total Repayment Amount(€) ", ).grid(sticky='w', row=12, column=1, columnspan=3)
        self.totalRepaymentAmountVar = tk.StringVar()
        tk.Label(frame, height=2, width=20, textvariable=self.totalRepaymentAmountVar).grid(row=12, column=4)

        # 消息循环
        self.window.mainloop()

    # 按钮点击监听
    def calculate(self):
        loanInfo = {
            'First time buyer': {'loanToValue': 0.9, 'requiredDeposit': 0.1, 'interestRate': 2.6, 'incomeToMu': 3.5},
            'Returning buyer': {'loanToValue': 0.8, 'requiredDeposit': 0.2, 'interestRate': 3, 'incomeToMu': 3.5},
            'Buy-to-Let': {'loanToValue': 0.7, 'requiredDeposit': 0.3, 'interestRate': 4, 'incomeToMu': 2}}

        # 获取输入的参数
        income = eval(self.income.get())
        propertyCost = eval(self.propertyCost.get())
        loanType = self.loanType.get()
        loanTerm = int(self.loanTerm.get())

        isIncomeSatisfied = False
        if income * loanTerm >= propertyCost * loanInfo[loanType]['incomeToMu']:  # 年收入*贷款年限 >= 房屋价值*收入与价值的倍数 才可以获得贷款
            isIncomeSatisfied = True
        if isIncomeSatisfied:
            self.isIncomeSatisfiedVar.set('Congratulations, your income meets the purchase need!')

            # 计算所需存款现金金额
            requiredCash = propertyCost * loanInfo[loanType]['requiredDeposit']  # 这个相当于是首付
            self.requiredCashVar.set(format(requiredCash, '.2f'))

            # 计算总还款金额
            totalRepaymentAmount = loanInfo[loanType]['loanToValue'] * (propertyCost + loanInfo[loanType]['interestRate'] / 100 * loanTerm)  # 还款金额 = 贷款金额+利息
            self.totalRepaymentAmountVar.set(format(totalRepaymentAmount, '.2f'))
        else:
            self.isIncomeSatisfiedVar.set('Sorry, your income does not meet the purchase need!')
            self.requiredCashVar.set("")
            self.totalRepaymentAmountVar.set("")


if __name__ == '__main__':
    LoanCalculator()
    pass
