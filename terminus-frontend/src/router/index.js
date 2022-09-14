import Vue from 'vue';
import VueRouter from 'vue-router';

// LAYOUTS
import Layout from '../layouts/Layout';

// VIEWS
import JoinGame from '../views/JoinGame.vue';
import Home from '../views/Home';
import About from '../views/About';
import QuizzForm from '../views/QuizzForm.vue';
import Quizz from '../views/Quizz.vue';
import MyAccount from '../views/MyAccount';
import NotFound from '../views/NotFound';
import CreateGame from '../views/CreateGame'
import GenerateQuiz from '../views/GenerateQuiz'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Root',
    redirect: '/terminus'
  },
  {
    path: '/terminus',
    name: "Layout",
    component: Layout,
    redirect: '/terminus/home',
    meta: {
      checkAuth: true,
      title: "Terminus",
    },
    children: [
      {
        path: '/terminus/home',
        name: 'Home',
        component: Home
      },
      {
        path: '/terminus/quizz',
        name: 'Quizz',
        component: Quizz,
        redirect: '/terminus/quizz/create',
        children: [
          {
            path: '/terminus/quizz/create',
            name: 'QuizzCreation',
            component: QuizzForm,
            meta: {
              requiresAuth: true,
              title: "Terminus",
            }
          },
          {
            path: '/terminus/quizz/:id',
            props: true,
            name: 'QuizzUpdate',
            component: QuizzForm,
            meta: {
              requiresAuth: true,
              title: "Terminus",
            }
          }
        ]
      },
      {
        path: '/terminus/game/join',
        name: 'JoinGame',
        component: JoinGame,
        meta: {
          title: "Terminus",
        }
      },
      {
        path: '/terminus/game/create/',
        props: true,
        name: 'CreateGame',
        component: CreateGame,
        meta: {
          requiresAuth: true,
          title: "Terminus",
        }
      },
      {
        path: '/terminus/about',
        name: 'About',
        component: About
      },
      {
        path: '/terminus/my-account',
        name: 'MyAccount',
        component: MyAccount,
        meta: {
          requiresAuth: true,
          title: "Terminus"
        },
      },
      {
        path: '/terminus/quiz/generate_quiz',
        name: 'GenerateQuiz',
        component: GenerateQuiz,
        meta: {
          title: "Terminus",
        }
      },
      {
        path: '/terminus/*',
        name: 'NotFound',
        component: NotFound
      }
    ]
  }
];

export default routes
