import {
  createNavigator,
  SwitchRouter,
} from "@react-navigation/core";
import { createBrowserApp } from "@react-navigation/web";
import AppView from "./AppView";
import Intro from "./components/Intro";
import Camera from "./components/Camera";
import Message from "./components/Message";


const AppNavigator = createNavigator(
    AppView,
    SwitchRouter({
      Intro,
      Camera,
      Message
    }),
    {}

);

const AppNav = createBrowserApp(AppNavigator);

export default AppNav;
