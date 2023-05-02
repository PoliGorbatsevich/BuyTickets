import React from "react";
import {axiosInstance} from "../AxiosConfig";
import toast from "react-hot-toast";
import { Navigate } from "react-router-dom";
import Transaction from "../components/Transaction";

class Transactionpage extends React.Component{

    constructor(props) {
        super(props);
        this.state = {
            transactions:[],
            logined: true
        }
        axiosInstance.get("user_profile/transaction_history/")
            .then((res) => {
                console.log(res.data);
                this.setState({transactions: res.data, logined: true});
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
                        <div className="base-block">
                            <h1>История Транзакций</h1>
                            {this.state.transactions.map( el => (
                                <Transaction key={el.id} transaction={el}/>
                            ))}
                        </div>
                    </main>
                </div>
            )
        else
            return <Navigate to="../auth/"/>
    }

}

export default Transactionpage