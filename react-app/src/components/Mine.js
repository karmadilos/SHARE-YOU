import React, { Component, useEffect, useState } from 'react';
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import { Button } from 'react-bootstrap';
import axios from 'axios';

//https://www.npmjs.com/package/react-datepicker
import DatePicker from 'react-datepicker';
import "react-datepicker/dist/react-datepicker.css";

export function Mine() {
  return (
    <div>
      <h1>내 포트폴리오 보기</h1>
      <Education onCreate={function (data) { 
        axios.post(`http://127.0.0.1:5000/education`, data, {
          headers:{
            Authorization: "Bearer " + localStorage.getItem("token")
          }
        }); 
      }
        }  
        />
      <Awards onCreate={function (data) { 
        axios.post(`http://127.0.0.1:5000/awards`, data, {
          headers:{
            Authorization: "Bearer " + localStorage.getItem("token")
          }
        }); 
      }
        }  
        />
      <Projects onCreate={function (data) { 
        axios.post(`http://127.0.0.1:5000/projects`, data, {
          headers:{
            Authorization: "Bearer " + localStorage.getItem("token")
          }
        }); 
      }
        }  
        />
        <Certificates onCreate={function (data) { 
        axios.post(`http://127.0.0.1:5000/certificates`, data, {
          headers:{
            Authorization: "Bearer " + localStorage.getItem("token")
          }
        }); 
      }
        }  
        />
    </div>
  );
}
// https://react-bootstrap.github.io/components/accordion/ 플러스 버튼 이걸로 구현

function Education(props){
  return (
    <Form
          action=""
          method="post"
          onSubmit={function (e) {
            e.preventDefault();
            props.onCreate({
              college: e.target.college.value,
              major: e.target.major.value,
              degree: e.target.formHorizontalRadios.value
            });
            e.target.reset();
          }}
    >
      <h3>학력</h3>
      <article>
      - 학력: 학교이름, 전공 정보를 text 형식으로 입력받습니다.  
        학위에 대한 사항은 radio button을 통해 입력받습니다.
      </article>
      <Form.Group as={Row} controlId="formHorizontalCollege">
        <Form.Label column sm={2}>
        </Form.Label>
        <Col sm={10}>
          <Form.Control name="college" placeholder="학교이름" />
        </Col>
      </Form.Group>

      <Form.Group as={Row} controlId="formHorizontalMajor">
        <Form.Label column sm={2}>
        </Form.Label>
        <Col sm={10}>
          <Form.Control name="major" placeholder="전공" />
        </Col>
      </Form.Group>
      <fieldset>
        <Form.Group as={Row}>
          <Form.Label as="legend" column sm={2}>
            학위
          </Form.Label>
          <Col sm={10}>
            <Form.Check
              type="radio"
              label="재학중"
              name="formHorizontalRadios"
              id="formHorizontalRadios1"
              value="1"
            />
            <Form.Check
              type="radio"
              label="학사졸업"
              name="formHorizontalRadios"
              id="formHorizontalRadios2"
              value="2"
            />
            <Form.Check
              type="radio"
              label="석사졸업"
              name="formHorizontalRadios"
              id="formHorizontalRadios3"
              value="3"
            />
            <Form.Check
              type="radio"
              label="박사졸업"
              name="formHorizontalRadios"
              id="formHorizontalRadios4"
              value="4"
            />
          </Col>
        </Form.Group>
      </fieldset>

      <Form.Group as={Row}>
        <Col sm={{ span: 10, offset: 2 }}>
          <Button variant="primary" type="submit">
            저장
          </Button>
        </Col>
      </Form.Group>
    </Form>
  );
}

function Awards(props){
  return (
    <Form
    action=""
    method="post"
    onSubmit={function (e) {
      e.preventDefault();
      props.onCreate({
        award: e.target.award.value,
        detail: e.target.awardDetail.value
      });
      e.target.reset();
    }}
>
      <h3>수상이력</h3>
      <article>
      - 수상 이력: 수상 내역과 상세내역을 text 형식으로 입력받습니다.
      </article>
      <Form.Group as={Row} controlId="formHorizontalAward">
        <Form.Label column sm={2}>
        </Form.Label>
        <Col sm={10}>
          <Form.Control name="award" placeholder="수상내역" />
        </Col>
      </Form.Group>

      <Form.Group as={Row} controlId="formHorizontalAwardDetail">
        <Form.Label column sm={2}>
        </Form.Label>
        <Col sm={10}>
          <Form.Control name="awardDetail" placeholder="상세내역" />
        </Col>
      </Form.Group>

      <Form.Group as={Row}>
        <Col sm={{ span: 10, offset: 2 }}>
          <Button variant="primary" type="submit">
            저장
          </Button>
        </Col>
      </Form.Group>
    </Form>
  );
}
function formDate(){ //날짜형식 yyyy-mm-dd로 바꿔주기
  var date = new Date();
  var year = date.getFullYear();
  var month = ("0" + (1 + date.getMonth())).slice(-2);
  var day = ("0" + date.getDate()).slice(-2);

  return year + "-" + month + "-" + day;
}

function Projects(props){
  const [startDate, setStartDate] = useState(new Date("2021/02/24"));
  const [endDate, setEndDate] = useState(new Date("2021/02/24"));
  console.log(formDate(startDate));
  return (
    <Form
          action=""
          method="post"
          onSubmit={function (e) {
            e.preventDefault();
            props.onCreate({
              project: e.target.project.value,
              detail: e.target.projectDetail.value,
              startDate: formDate(startDate),
              endDate: formDate(endDate)
            });
            e.target.reset();
          }}
    >
      <h3>프로젝트</h3>
      <article>
      - 프로젝트: 프로젝트 이름과 상세내역을 txt 형식으로 입력받습니다. 
      -프로젝트 수행기간은 datepicker를 활용해 날짜(년월일)를 입력받습니다.
      </article>
      <Form.Group as={Row} controlId="formHorizontalProject">
        <Form.Label column sm={2}>
        </Form.Label>
        <Col sm={10}>
          <Form.Control name="project" placeholder="프로젝트" />
        </Col>
      </Form.Group>

      <Form.Group as={Row} controlId="formHorizontalProjectDetail">
        <Form.Label column sm={2}>
        </Form.Label>
        <Col sm={10}>
          <Form.Control name="projectDetail" placeholder="프로젝트상세" />
        </Col>
      </Form.Group>

      <DatePicker selected={startDate} onChange={date => setStartDate(date)} />
      <DatePicker 
        selected={endDate} 
        onChange={date => setEndDate(date)} 
        minDate={startDate}/>

      <Form.Group as={Row}>
        <Col sm={{ span: 10, offset: 2 }}>
          <Button variant="primary" type="submit">
            저장
          </Button>
        </Col>
      </Form.Group>
    </Form>
  );
}

function Certificates(props){
  const [startDate, setStartDate] = useState(new Date());
  return (
    <Form
          action=""
          method="post"
          onSubmit={function (e) {
            e.preventDefault();
            props.onCreate({
              certificate: e.target.certificate.value,
              organization: e.target.organization.value,
              get_date: formDate(startDate)
            });
            e.target.reset();
          }}
    >
      <h3>자격증</h3>
      <article>
      - 자격증: 자격증 이름, 공급기관을 text 형식으로 입력받습니다. 
      -취득일자는 datepicker를 활용해 날짜(년월일)를 입력받습니다.
      </article>
      <Form.Group as={Row} controlId="formHorizontalCertificate">
        <Form.Label column sm={2}>
        </Form.Label>
        <Col sm={10}>
          <Form.Control type="certificate" placeholder="자격증이름" />
        </Col>
      </Form.Group>

      <Form.Group as={Row} controlId="formHorizontalOrganization">
        <Form.Label column sm={2}>
        </Form.Label>
        <Col sm={10}>
          <Form.Control type="organization" placeholder="발급기관" />
        </Col>
      </Form.Group>

      <h6>취득일</h6>
      <DatePicker selected={startDate} onChange={date => setStartDate(date)} />

      <Form.Group as={Row}>
        <Col sm={{ span: 10, offset: 2 }}>
          <Button variant="primary" type="submit">
            저장
          </Button>
        </Col>
      </Form.Group>
    </Form>
  );
}