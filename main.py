from controllers.FinanceController import FinanceController
from models.FinanceModel import FinanceModel
from views.FinanceView import FinanceView

if __name__ == "__main__":
    model = FinanceModel()
    view = FinanceView()

    controller = FinanceController(model, view)


    view.mainloop()


