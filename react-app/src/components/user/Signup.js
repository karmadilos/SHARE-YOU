import React, { useState } from 'react';
import axios from 'axios';
import { Button, Alert } from 'react-bootstrap';
import Form from 'react-bootstrap/Form';
import * as config from '../../config';

export default function Signup({history}) {
  const [signed,setSigned] = useState('');
  if (signed === 'success'){
    setSigned('');
    alert('회원가입 성공!');
    history.push('/login');
  }
  return (
    <div>
      <h1>회원가입</h1>
      <SignupForm onCreate={function (data) { 
        axios.post(config.API_HOST +`/signup`, data)
        .then(response=>{setSigned(response.data.status)}); 
        }} />
    </div>
  );
}

function SignupForm(props) {
  //https://dog-developers.tistory.com/109 비밀번호 재사용
  const [password,setPassword] = useState('');
  const [passwordError,setPasswordError] = useState(false);

  return (
    <article>
      <form
        action=""
        method="post"
        onSubmit={function (e) {
          e.preventDefault();
          props.onCreate({
            fullname: e.target.formBasicName.value,
            email: e.target.formBasicEmail.value,
            password: e.target.formBasicPassword.value
          });
          e.target.reset();
        }}
      >
        <Form.Group controlId="formBasicEmail">
          <Form.Label>Email address</Form.Label>
          <Form.Control type="email" placeholder="Enter email" name="formBasicEmail" />
          <Form.Text className="text-muted">
            Check your email.
          </Form.Text>
        </Form.Group>
        <Form.Group controlId="formBasicPassword">
          <Form.Label>Password</Form.Label>
          <Form.Control 
            type="password" 
            placeholder="Password" 
            name="formBasicPassword"
            value={password}
            required
            onChange={(e) => setPassword(e.target.value)} 
            />
        </Form.Group>
        <Form.Group controlId="formBasicPasswordConfirm">
          <Form.Label>Confirm Password</Form.Label>
          <Form.Control 
            type="password" 
            placeholder="Password"
            onChange={(e)=>setPasswordError(e.target.value !== password)} />
        </Form.Group>
        <Form.Text className="text-muted">
          {passwordError && <div style={{color : 'red'}}>비밀번호가 일치하지 않습니다.</div>}
        </Form.Text>
        <Form.Group controlId="formBasicName">
          <Form.Label>Name</Form.Label>
          <Form.Control type="text" placeholder="Name" name="formBasicName" />
        </Form.Group>

        <Button variant="primary" type="submit">
          회원가입
        </Button>
      </form>
    </article>
  );
}