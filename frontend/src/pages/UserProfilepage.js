import React from "react";
import {axiosInstance} from "../AxiosConfig";
import {MdDeleteForever} from "react-icons/md";
import ChangePassword from "../components/ChangePassword";
import Payment from "../components/Payment";
import {AiFillInfoCircle} from "react-icons/ai";
import toast from "react-hot-toast";
import { Navigate } from "react-router-dom";

class UserProfilepage extends React.Component{

    constructor(props) {
        super(props);
        this.state = {
            profile: {},
            tickets: [],
            logined: true
        }
        axiosInstance.get("user_profile/me")
            .then((res) => {
                console.log(res.data);
                this.setState({profile: res.data, logined: true});
            }).catch(err => {
                this.setState({logined: false});
                toast("Давайте сначала авторизуемся");
        });
    }
    render(){
        if (this.state.logined)
            return (
                <div>
                    <main>
                        <div className="profile">
                            <h1>Ваш профиль</h1>
                            <h2>Имя: {this.state.profile.username}</h2>
                            <h2>Почта: {this.state.profile.email}</h2>
                            <h2>Роль: {this.state.profile.role}</h2>
                            <h2>Баланс: {this.state.profile.balance}</h2>
                        </div>
                        <Payment topUpBalance={this.topUpBalance}/>
                        <ChangePassword changePass={this.changePass}/>
                    </main>
                    <aside>
                        <MyTickets/>
                    </aside>
                </div>
            )
        else
            return <Navigate to="../auth/"/>
    }

    changePass(old_password, password, password1){
        const ulrParams = new URLSearchParams({
            old_pass: old_password,
            new_pass: password,
            new_pass1: password1
        })
        axiosInstance.post("/user_profile/change_password", {},{
            params: ulrParams
        })
            .then((res) => {
                toast.success("Пароль обновлен, постарайтесь его не забыть")
                console.log(res.data)
            }).catch(err => toast.error("Вы ввели неправильные данные"))
    }

    topUpBalance(payment){
        const ulrParams = new URLSearchParams({
            payment: payment,
        })
        axiosInstance.post("/user_profile/top_up_balance", {},{
            params: ulrParams
        })
            .then((res) => {
                toast.success("Баланс пополнен!")
                toast("Обновите страницу, чтобы увидеть актуальный баланс")
                console.log(res.data)
            }).catch(err => toast.error("Похоже вы ввели данные неправильно"))
    }

}


class MyTickets extends React.Component{

    performance = {}
    constructor(props) {
        super(props);
        this.state = {
            tickets:[],
        }
        axiosInstance.get("user_profile/my_tickets")
            .then((res) => {
                console.log(res.data)
                this.setState({tickets: res.data})
            }).catch(err => null)
        this.returnTicket = this.returnTicket.bind(this)
    }
    render(){
        return (
            <div className="base-block">
                <h1>My tickets</h1>
                {this.state.tickets.map( el => (
                    <MyTicket key={el.id} ticket={el} onReturn={this.returnTicket}/>
                ))}
            </div>
        )
    }

    returnTicket(id){
        axiosInstance.post("user_profile/my_tickets/"+id+"/return_ticket")
            .then((res) => {
                if (res.status === 200) {
                    toast.success("Вы вернули билет")
                    toast("Обновите страницу, чтобы увидеть актуальный баланс")
                    this.setState({
                        tickets: this.state.tickets.filter((el) => el.id !== id)
                    })
                }
            }).catch(err => toast.error("Вы не можете вернуть билет, который недействителен"))
    }

}

class MyTicket extends React.Component{

    performance = {}
    constructor(props) {
        super(props);
        this.state = {
            ticket:{},
            performance:{},
            show_performance: false
        }
    }
    render(){
        return (
            <div className="ticket">
                <MdDeleteForever className="delete-icon" onClick={() =>
                    this.props.onReturn(this.props.ticket.id)}/>
                <AiFillInfoCircle className="info-icon" onClick={() =>{
                    this.setState({show_performance: !this.state.show_performance})
                    axiosInstance.get("/performance/"+this.props.ticket.performance_id)
                        .then((res) => {
                            console.log(res.data)
                            res.data.time = res.data.time.slice(0, 5);
                            this.setState({performance:res.data})
                        })
                    }}/>
                {this.state.show_performance && <div>
                    <h3>Название: {this.state.performance.name}</h3>
                    <h4>Дата: {this.state.performance.date}</h4>
                    <h4>Время: {this.state.performance.time}</h4>
                    <p>Описание: {this.state.performance.description}</p><br/>
                </div>}
                <h3>ряд: {this.props.ticket.row_number} место: {this.props.ticket.place_number}</h3>
                <p>цена: {this.props.ticket.price}</p>
            </div>
        )
    }
}

export default UserProfilepage