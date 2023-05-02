import React from "react";
import {MdDeleteForever} from "react-icons/md"
import {GiAutoRepair} from "react-icons/gi"
import PerformanceUpdateForm from "./PerformanceUpdateForm";
import TicketsMap from "./TicketsMap";
import storage from "../storage";

class Performance extends React.Component{
    constructor(props) {
        super(props);
        this.state = {
            editForm: false,
            showTickets: false
        }
    }
    performance = this.props.performance
    render() {
        return (
            <div className="performance">
                {storage.getRole() === "admin" &&
                <MdDeleteForever className="delete-icon" onClick={() =>
                    this.props.onDelete(this.performance.id)}/>}
                {storage.getRole() === "admin" &&
                <GiAutoRepair className="update-icon" onClick={() =>{
                    this.setState({editForm: !this.state.editForm})}}/>}
                <div onClick={() =>{
                    this.setState({showTickets: !this.state.showTickets})}}>
                    <h3>Название: {this.performance.name} Дата: {this.performance.date} Время: {this.performance.time.slice(0, 5)}</h3>
                    <p>Описание: {this.performance.description}</p>
                </div>
                {this.state.editForm && <PerformanceUpdateForm id={this.performance.id} onUpdate={this.props.onUpdate}/>}
                {this.state.showTickets && <TicketsMap id={this.performance.id} />}
            </div>
        )
    }
}

export default Performance