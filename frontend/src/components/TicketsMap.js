import React from "react";
import {axiosInstance} from "../AxiosConfig";
import {MdDeleteForever} from "react-icons/md";
import {TfiMoney} from "react-icons/tfi"
import toast from "react-hot-toast";
import storage from "../storage";

class TicketsMap extends React.Component{
    performance = {}
    constructor(props) {
        super(props);
        this.state = {
            tickets:[]
        }
        axiosInstance.get("performance/"+this.props.id+"/ticket")
            .then((res) => {
                console.log(res.data)
                this.setState({tickets: res.data})
            })
        this.deleteTicket = this.deleteTicket.bind(this)
    }


    render(){
        return (
            <div>
                {this.state.tickets.map( el => (
                    <Ticket key={el.id} ticket={el}
                        onBuy={this.buyTicket}
                        onDelete={this.deleteTicket}/>
                ))}
            </div>
        )
    }

    buyTicket(ticket_id) {
        axiosInstance.post("ticket/"+ticket_id+'/buy'
            ).then((response) => {
            if (response.status === 200) {
                toast.success("Вы купили билет!")
                toast("Вы можете найти его в профиле!")
            }
        }).catch(err =>{
            toast.error("У вас недостаточно денег или этот билет уже кем-то преобретен!")
            toast("Попробуйте обновить сайт или проверить баланс в профиле")
        })
    }

    deleteTicket(id) {
        axiosInstance.delete("ticket/" + id)
            .then((response) => {
                toast.success("Билет удален!")
                if (response.status === 200)
                    this.setState({
                        tickets: this.state.tickets.filter((el) => el.id !== id)
                    })
            })
    }
}

class Ticket extends React.Component{
    constructor(props) {
        super(props);
        this.state = {
            ticket: {
                row_number:'',
                place_number:'',
                price:'',
            },
            buy_ticket:false
        }
    }

    ticket = this.props.ticket

    render() {
        if(!this.ticket.owner_id)
            return (
                <div className="ticket-free">

                    {storage.getRole()==="admin" && <MdDeleteForever className="delete-icon" onClick={() =>
                        this.props.onDelete(this.ticket.id)}/>}
                    <TfiMoney className="buy-icon" onClick={() =>
                        this.props.onBuy(this.ticket.id)}/>
                    <h3>ряд: {this.ticket.row_number} место: {this.ticket.place_number}</h3>
                    <p>цена: {this.ticket.price}</p>
                </div>
            )
        else
            return (
                <div className="ticket">
                    {storage.getRole()==="admin" &&
                    <MdDeleteForever className="delete-icon" onClick={() =>
                        this.props.onDelete(this.ticket.id)}/>}

                    <h3>ряд: {this.ticket.row_number} место:{this.ticket.place_number}</h3>
                    <p>цена: {this.ticket.price}</p>
                </div>
            )
    }
}

export default TicketsMap