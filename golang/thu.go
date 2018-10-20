//
// thu.go
// Copyright (C) 2018 Yongwen Zhuang <zeoman@163.com>
//
// Distributed under terms of the MIT license.
//

package main

import (
	"bytes"
	"crypto/md5"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"net/url"
	"os"
	"strconv"
	"strings"
)

func Check() {
	res, err := http.PostForm("https://net.tsinghua.edu.cn/do_login.php", url.Values{"action": {"check_online"}})
	if err != nil {
		log.Fatal(err)
	}
	defer res.Body.Close()

	content, err := ioutil.ReadAll(res.Body)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(string(content))
	if string(content) != "not_online" {
		res, err := http.Post("https://net.tsinghua.edu.cn/rad_user_info.php", "application/text", bytes.NewBuffer([]byte("")))
		if err != nil {
			log.Fatal(err)
		}
		defer res.Body.Close()
		content, err := ioutil.ReadAll(res.Body)
		if err != nil {
			log.Fatal(err)
		}
		info := strings.Split(string(content), ",")
		traffic, err := strconv.Atoi(info[6])
		if err != nil {
			log.Fatal(err)
		}
		traffic_f := float64(traffic) / 1000000000
		end, err := strconv.Atoi(info[2])
		if err != nil {
			log.Fatal(err)
		}
		start, err := strconv.Atoi(info[1])
		if err != nil {
			log.Fatal(err)
		}
		timelen := end - start
		time_str := fmt.Sprintf("%02d:%02d:%02d", timelen/3600, timelen/60%60, timelen%60)
		fmt.Printf("ip=%s, user=%s, traffic=%.2fGB, timelen=%s\n", info[8], info[0], traffic_f, time_str)
	}
}

func Login() {
	password_md5 := md5.Sum([]byte("password"))
	password := fmt.Sprintf("{MD5_HEX}%x", password_md5)
	data := url.Values{
		"action":   {"login"},
		"username": {"username"},
		"password": {password},
		"ac_id":    {"1"},
	}
	res, err := http.PostForm("https://net.tsinghua.edu.cn/do_login.php", data)
	if err != nil {
		log.Fatal(err)
	}
	defer res.Body.Close()

	content, err := ioutil.ReadAll(res.Body)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(string(content))
}

func Logout() {
	data := url.Values{
		"action": {"logout"},
	}
	res, err := http.PostForm("https://net.tsinghua.edu.cn/do_login.php", data)
	if err != nil {
		log.Fatal(err)
	}
	defer res.Body.Close()

	content, err := ioutil.ReadAll(res.Body)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(string(content))
}

func main() {
	if len(os.Args) < 3 {
		Check()
	} else {
		arg := os.Args[2]
		if arg == "login" {
			Login()
		} else if arg == "logout" {
			Logout()
		}
	}
}
