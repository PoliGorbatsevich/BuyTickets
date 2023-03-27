import React from "react";
import RegistrationForm from "../components/RegistrationForm";
import {axiosInstance} from "../AxiosConfig";
import LogInForm from "../components/LogInForm";
import storage from "../storage"
import toast from "react-hot-toast";
import {Navigate} from "react-router-dom";

const registration_url = "auth/registration"
const login_url = "auth/token"


class Authpage extends React.Component{
    constructor(props) {
        super(props);
        this.state = {
            user: {},
            loginForm: true,
            isLogined: false
        }
        this.registerUser = this.registerUser.bind(this)
        this.loginUser = this.loginUser.bind(this)
    }

    render(){
        if(!this.state.isLogined)
            return(
                <div>
                    <main>
                        <div className="info">
                        <h1>BuyTickets</h1>
                        <h2>Вы любите театр и часто посещаете его спектакли? Тогда наверняка вы знаете, как важно заранее приобрести билеты, чтобы не оказаться без них перед началом представления. Сегодня существует множество приложений для продажи билетов в театры, которые позволяют быстро и удобно выбрать места и оплатить билеты онлайн. Благодаря таким приложениям вы можете быть уверены, что ваше место на спектакле будет зарезервировано заранее, а вы сможете спокойно наслаждаться представлением в уютной атмосфере театрального зала. Попробуйте использовать одно из таких приложений и оцените все преимущества онлайн-покупки билетов в театр!</h2>
                        </div>
                    </main>
                    <aside>
                        {this.state.loginForm ?
                            <LogInForm loginUser={this.loginUser}/> :
                            <RegistrationForm registerUser={this.registerUser}/>
                        }
                        {this.state.loginForm ?
                            <button type="button" onClick={() =>{
                                this.setState({loginForm: !this.state.loginForm})
                                }}>У меня еще нет аккаунта</button>:
                            <button type="button" onClick={() =>{
                                this.setState({loginForm: !this.state.loginForm})
                            }}>У меня уже есть аккаунт</button>
                        }
                    </aside>
                </div>
            )
        else
            return(<Navigate to="/performance"/>)
    }

    registerUser(user){
        if (user.username.length === 0 || user.password.length === 0 || user.email.length === 0 || user.password1.length === 0){
            toast.error("данные введены некорректно")
        }
        else {
            axiosInstance.post(registration_url, user)
                .then((response) => {
                    toast("Поздравляем! Вы успешно зарегистрировались", {icon: '🥳'})
                    this.setState({loginForm: !this.state.loginForm})
                    this.setState({isLogined: true})
                }).catch(err => {
                toast.error(err.response.data.detail)
                this.setState({isLogined: false})
            })
        }
    }

    loginUser(user){
        if (user.username.length === 0 || user.password.length === 0){
            toast.error("данные введены некорректно")
        }
        else {
            axiosInstance.post(login_url,
                new URLSearchParams({
                    username: user.username,
                    password: user.password,
                })).then((response) => {
                toast("Ура! Вы снова с нами!", {icon: '☺️'})
                storage.setToken(response.data['access_token'])
                storage.setRole(response.data['role'])
                console.log(response.data);
                this.setState({isLogined: true})
            }).catch(err => {
                toast.error(err.response.data.detail)
            })
        }
    }
}

export default Authpage