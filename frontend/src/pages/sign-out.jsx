import {useEffect} from "react";
import {useNavigate} from 'react-router-dom';


export default function SignOut() {
    const navigate = useNavigate()
    useEffect(() => {
        fetch("/sign-out", {method: 'GET'})
            .then(res => {
                navigate('/')
                window.location.reload()
            })
    }, [])
}