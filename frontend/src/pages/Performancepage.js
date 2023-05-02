import React from "react";
import Performances from "../components/Performances";
import PerformanceForm from "../components/PerformanceForm";
import {axiosInstance} from "../AxiosConfig";
import storage from "../storage";
import toast from "react-hot-toast";
import {Navigate} from "react-router-dom";
import FilterForm from "../components/FilterForm";


class Performancepage extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            performances: [],
            logined: true
        }

        axiosInstance.get("performance").then((res) => {
            console.log(res.data)
            this.setState({performances: res.data, logined: true})
        }).catch(err => {
            toast("Давайте сначала авторизуемся")
            this.setState({logined: false})
        })
        this.getPerformances = this.getPerformances.bind(this)
        this.findByDate = this.findByDate.bind(this)
        this.addPerformance = this.addPerformance.bind(this)
        this.deletePerformance = this.deletePerformance.bind(this)
        this.updatePerformance = this.updatePerformance.bind(this)
    }

    render() {
        if(this.state.logined)
            return (
                <div>
                    <main>
                        <Performances performances={this.state.performances}
                                      onDelete={this.deletePerformance}
                                      onUpdate={this.updatePerformance}/>
                    </main>
                    <aside>
                        {storage.getRole() === "admin" &&
                        <PerformanceForm onAdd={this.addPerformance}/>}
                        <FilterForm onFind={this.findByDate} onClear={this.getPerformances}/>
                    </aside>
                </div>

            )
        else
            return <Navigate to="../auth/"/>
    }

    getPerformances(){
        axiosInstance.get("performance").then((res) => {
            console.log(res.data)
            this.setState({performances: res.data, logined: true})
        }).catch(err => {
            toast("Давайте сначала авторизуемся")
            this.setState({logined: false})
        })
    }

    addPerformance(perf, price, row_length, row_count) {
        const ulrParams = new URLSearchParams({
            row_count: row_count,
            row_length: row_length,
            price: price
        })
        axiosInstance.post("performance/create",
            perf,
            {
                params: ulrParams
            }).then((response) => {
            if (response.status === 200) {
                perf['id'] = response.data
                console.log(response.data)
                this.setState({
                    performances: [...this.state.performances, {...perf}]
                })
                toast.success("Пьеса была создана!")
            }
        }).catch(err =>{
            toast.error("Вы ввели некорректные данные!")})
    }

    deletePerformance(id) {
        axiosInstance.delete("performance/" + id + "/delete")
            .then((response) => {
                if (response.status === 200)
                    toast.success("Пьеса была удалена")
                    this.setState({
                        performances: this.state.performances.filter((el) => el.id !== id)
                    })
            })
    }

    findByDate(date) {
        const ulrParams = new URLSearchParams({
            date:date
        })
        axiosInstance.get("performance/playbill/", {params:ulrParams})
            .then((response) => {
                if (response.status === 200)
                    toast.success("Вот все что мы нашли на дату: "+date)
                this.setState({
                    performances: response.data
                })
            }).catch(err => toast.error("Вы ввели неверные данные"))
    }

    updatePerformance(id, perf) {
        let allPerformances = this.state.performances
        axiosInstance.post("performance/" + id + "/update", perf)
            .then((response) => {
                if (response.status === 200) {
                    for (let i = 0; i < allPerformances.length; i++)
                        if (allPerformances[i].id === id) {
                            allPerformances[i].name = perf.name
                            allPerformances[i].description = perf.description
                            allPerformances[i].date = perf.date
                            allPerformances[i].time = perf.time
                        }
                    this.setState({performances: []})
                    this.setState({performances: [...allPerformances]})
                    toast.success("Пьеса обновлена!")
                    console.log(this.props.performances)
                }
            }).catch(err =>{
            toast.error("Вы ввели неправильные данные или не ввели какие-то поля!")
            })
    }
}

export default Performancepage