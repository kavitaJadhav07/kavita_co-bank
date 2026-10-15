
    def check_balance(self):
        account = self.authenticate()
        if account:
            print(f"Available balance: ₹{account.balance:.2f}")

    def deposit(self):
        account = self.authenticate()
        if not account:
            return
        try:
            amount = round(float(input("Deposit amount: ₹").strip()), 2)
            if amount <= 0 or amount == float("inf") or amount != amount:
                print("Enter a valid amount greater than zero.")
                return
        except ValueError:
            print("Please enter a valid amount.")
            return
        account._change_balance(amount)
        account.add_transaction("Deposit", amount)
        self.save_data()
        print(f"Deposit successful. New balance: ₹{account.balance:.2f}")

    def withdraw(self):
        account = self.authenticate()
        if not account:
            return
        try:
            amount = round(float(input("Withdrawal amount: ₹").strip()), 2)
            if amount <= 0 or amount == float("inf") or amount != amount:
                print("Enter a valid amount greater than zero.")
                return
        except ValueError:
            print("Please enter a valid amount.")
            return
        if amount > account.balance:
            print("Insufficient balance.")
            return
        account._change_balance(-amount)
        account.add_transaction("Withdrawal", -amount)
        self.save_data()
        print(f"Withdrawal successful. New balance: ₹{account.balance:.2f}")

    def transfer(self):
        sender = self.authenticate()
        if not sender:
            return
        recipient_number = input("Recipient account number: ").strip()
        recipient = self.accounts.get(recipient_number)
        if recipient is None:
            print("Recipient account not found.")
            return
        if recipient.account_number == sender.account_number:
            print("You cannot transfer money to the same account.")
            return
        try:
            amount = round(float(input("Transfer amount: ₹").strip()), 2)
            if amount <= 0 or amount == float("inf") or amount != amount:
                print("Enter a valid amount greater than zero.")
                return
        except ValueError:
            print("Please enter a valid amount.")
            return
        if amount > sender.balance:
            print("Insufficient balance.")
            return

        # Update both accounts and record each side of the transfer.
        sender._change_balance(-amount)
        recipient._change_balance(amount)
        sender.add_transaction("Transfer sent", -amount, f"To account {recipient.account_number}")
        recipient.add_transaction("Transfer received", amount, f"From account {sender.account_number}")
        self.save_data()
        print(f"Transfer successful. New balance: ₹{sender.balance:.2f}")

    def transaction_history(self):
        account = self.authenticate()
        if not account:
            return
        print("\n--- Transaction History ---")
        if not account.transactions:
            print("No transactions found.")
            return
        for item in account.transactions:
            print(
                f"{item['date_time']} | {item['type']} | "
                f"Amount: ₹{item['amount']:.2f} | "
                f"Balance: ₹{item['balance_after']:.2f}"
                + (f" | {item['note']}" if item.get("note") else "")
            )

    def change_pin(self):
        account = self.authenticate()
        if not account:
            return
        new_pin = input("Enter new 4–6 digit PIN: ").strip()
        if not valid_pin(new_pin):
            print("PIN must contain 4–6 digits.")
            return
        confirm_pin = input("Confirm new PIN: ").strip()
        if new_pin != confirm_pin:
            print("PINs do not match.")
            return
        if account.verify_pin(new_pin):
            print("New PIN must be different from the current PIN.")
            return
        account.set_pin(new_pin)
        self.save_data()
        print("PIN changed successfully.")

    def close_account(self):
        account = self.authenticate()
        if not account:
            return
        if account.balance != 0:
            print(f"Account cannot be closed. Withdraw or transfer the remaining ₹{account.balance:.2f} first.")
            return
        confirmation = input("Type CLOSE to confirm account closure: ").strip()
        if confirmation != "CLOSE":
            print("Account closure cancelled.")
            return
        del self.accounts[account.account_number]
        self.save_data()
        print("Account closed successfully.")

    def run(self):
        while True:
            print(f"\n{'=' * 15} {BANK_NAME} {'=' * 15}")
            print("1. Create Account")
            print("2. Account Details")
            print("3. Deposit Money")
            print("4. Withdraw Money")
            print("5. Check Balance")
            print("6. Transfer Money")
            print("7. Transaction History")
            print("8. Change PIN")
            print("9. Close Account")
            print("10. Exit")
            choice = input("Choose an option (1–10): ").strip()

            actions = {
                "1": self.create_account,
                "2": self.account_details,
                "3": self.deposit,
                "4": self.withdraw,
                "5": self.check_balance,
                "6": self.transfer,
                "7": self.transaction_history,
                "8": self.change_pin,
                "9": self.close_account,
            }
            if choice == "10":
                print("Thank you for using SmartTrust Bank. Goodbye!")
                break
            action = actions.get(choice)
            if action:
                try:
                    action()
                except (OSError, json.JSONDecodeError) as error:
                    print(f"Could not save or read bank data: {error}")
