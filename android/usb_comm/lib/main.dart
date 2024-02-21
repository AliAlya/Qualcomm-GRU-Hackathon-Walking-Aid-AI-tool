import 'dart:async';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(MyApp());
}

class MyApp extends StatefulWidget {
  @override
  _MyAppState createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  String _message = 'Waiting for response...';
  Timer? _timer;

  @override
  void initState() {
    super.initState();
    _startRepeatingTask();
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  void _startRepeatingTask() {
    // Setting up a periodic timer to call the API every 5 seconds
    _timer = Timer.periodic(Duration(seconds: 1), (timer) async {
      await _makeApiCall();
    });
  }

Future<void> _makeApiCall() async {
  try {
    final response = await http.get(Uri.parse('https://v6ma9h036i.execute-api.us-east-1.amazonaws.com/default/gait?id=1'));
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      setState(() {
        // Extracting the 'value' field from the JSON object
        _message = "Probability Suboptimal Gait = ${data['value']}";
      });
    } else {
      setState(() {
        _message = 'Error: ${response.statusCode}';
      });
    }
  } catch (e) {
    setState(() {
      _message = 'Error: ${e.toString()}';
    });
  }
}


  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        body: Center(
          child: Text(_message),
        ),
      ),
    );
  }
}
