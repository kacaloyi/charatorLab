from manager.define import Chat


class ChatAgent(Chat):
    def __init__(self, sessionid,room_template,histroy,option):
        super().__init__(sessionid,room_template,histroy,option)

    def _create(self,room_template:str,history:list,option:dict):
        return

    def _predict(self, input:str):
        # do prediction here based on room type

       
        return 
