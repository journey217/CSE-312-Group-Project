import {useEffect, useState} from "react";
import { Link, useNavigate } from 'react-router-dom';


export default function SignOut(page) {

    const navigate = useNavigate()
    useEffect(() => {
        fetch("/sign-out", {method: 'GET'})
            .then(res => {
                navigate('/')
            })
    }, [])
}