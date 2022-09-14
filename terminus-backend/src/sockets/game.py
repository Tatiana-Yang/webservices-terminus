class QuizGame:
    def __init__(self,id_quiz):
        self.players = {}
        self.id_quiz = id_quiz
        self.question_num = 0
        self.current_answer = []
        self.scores = {}  
        self.ans_queue = [] 
        self.ans_recieved = 0
        self.players_alive = 0
        self.question ={}
        self.public_call_stats = {}

    def register_player(self, pseudo):
        if pseudo in self.players :
            return -1
        else:
            self.players[pseudo] = 1 #1 means that the player has not been eliminated
            self.scores[pseudo] = 0 #initializing score of the player 
            self.players_alive +=1

    def register_eliminated(self,pseudo):
        self.players[pseudo] = 0 #set that the player has been eliminated
        #self.scores[pseudo] = 0 #score at 0 if eliminated #à voir et demander
        self.players_alive -=1

    def check_players_eliminated(self,pseudo):
        if self.players[pseudo] == 0:
            return -1
        return 0

    def get_all_pseudos(self):
        return self.players.keys()

    def get_id_quiz(self):
        return self.id_quiz

    def get_question_num(self):
        return self.question_num

    def get_scores(self):
        list_scores = []

        for key, value in self.scores.items():
            list_pseudo_score = []
            list_pseudo_score.append(key)
            list_pseudo_score.append(value)
            list_scores.append(list_pseudo_score)

        list_scores = sorted(list_scores, key=lambda x: x[1], reverse=True)

        return list_scores

    def get_scores_sorted(self):
        list_scores = []
        cpt = 0
        same_score=0

        for key, value in self.scores.items():
            list_pseudo_score = []
            list_pseudo_score.append(key)
            list_pseudo_score.append(value)
            list_scores.append(list_pseudo_score)

        list_scores = sorted(list_scores, key=lambda x: x[1], reverse=True)

        for elt in list_scores:
            if(same_score != elt[1]):
                cpt +=1
                same_score = elt[1]
            elt.insert(0,cpt)
        return list_scores[:10]

    def next_question_num(self):
        self.question_num += 1
        self.update_players_scores()
        self.reset_queue()
        self.ans_recieved = 0
        self.public_call_stats = {}

    def set_current_answers(self,ans):
        self.current_answer = ans

    def get_current_answers(self):
        return self.current_answer

    def update_players_scores(self):
        cpt = 3 
        for player in self.ans_queue:
            if cpt > 0:
                self.scores[player] += 5
                cpt -=1
            else:
                self.scores[player] += 3

    def add_player_in_queue(self,pseudo):
        self.ans_queue.append(pseudo)
    
    def get_total_alive(self):
        cpt =0
        for key in self.players:
            if(self.players[key] > 0):
                cpt +=1
        return cpt == self.ans_recieved or cpt < self.ans_recieved

    def reset_queue(self):
        self.ans_queue = []

    def get_current_question(self):
        return self.question

    def set_current_question(self,question):
        self.question = question

    def get_public_call_stats(self):
        return self.public_call_stats

    def set_public_call_stats(self,ans):
        self.public_call_stats[ans['answer']] = self.public_call_stats.get(ans['answer'], 0)+ 1