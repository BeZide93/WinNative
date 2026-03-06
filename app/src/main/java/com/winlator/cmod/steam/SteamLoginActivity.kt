package com.winlator.cmod.steam

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.animation.*
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.Visibility
import androidx.compose.material.icons.filled.VisibilityOff
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.winlator.cmod.steam.enums.LoginResult
import com.winlator.cmod.steam.enums.LoginScreen
import com.winlator.cmod.steam.ui.SteamLoginViewModel
import com.winlator.cmod.steam.ui.components.QrCodeImage
import timber.log.Timber

class SteamLoginActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        // Ensure SteamService is running
        try {
            val intent = android.content.Intent(this, com.winlator.cmod.steam.service.SteamService::class.java)
            startForegroundService(intent)
        } catch (e: Exception) {
            Timber.e(e, "Failed to start SteamService from SteamLoginActivity")
        }

        setContent {
            MaterialTheme(colorScheme = darkColorScheme()) {
                Surface(modifier = Modifier.fillMaxSize(), color = MaterialTheme.colorScheme.background) {
                    val viewModel: SteamLoginViewModel = viewModel()
                    LoginContent(viewModel)
                }
            }
        }
    }

    @OptIn(ExperimentalMaterial3Api::class)
    @Composable
    fun LoginContent(viewModel: SteamLoginViewModel) {
        val state by viewModel.loginState.collectAsState()
        var passwordVisible by remember { mutableStateOf(false) }

        LaunchedEffect(state.loginResult) {
            if (state.loginResult == LoginResult.Success) {
                Timber.i("User logged in, finishing activity")
                finish()
            }
        }

        Scaffold(
            topBar = {
                TopAppBar(
                    title = { Text("Steam Login") },
                    navigationIcon = {
                        if (state.loginScreen != LoginScreen.CREDENTIAL) {
                            IconButton(onClick = { viewModel.onShowLoginScreen(LoginScreen.CREDENTIAL) }) {
                                Icon(Icons.Default.ArrowBack, contentDescription = "Back")
                            }
                        }
                    }
                )
            }
        ) { padding ->
            Box(modifier = Modifier.fillMaxSize().padding(padding), contentAlignment = Alignment.Center) {
                Crossfade(targetState = state.loginScreen) { screen ->
                    when (screen) {
                        LoginScreen.CREDENTIAL -> CredentialLogin(state, viewModel, passwordVisible) { passwordVisible = !passwordVisible }
                        LoginScreen.QR -> QrLogin(state, viewModel)
                        LoginScreen.TWO_FACTOR -> TwoFactorLogin(state, viewModel)
                    }
                }
            }
        }
    }

    @Composable
    fun CredentialLogin(state: com.winlator.cmod.steam.ui.data.UserLoginState, viewModel: SteamLoginViewModel, passwordVisible: Boolean, onTogglePassword: () -> Unit) {
        var showRetryButton by remember { mutableStateOf(false) }
        
        LaunchedEffect(state.isSteamConnected) {
            if (!state.isSteamConnected) {
                kotlinx.coroutines.delay(15000)
                if (!state.isSteamConnected) {
                    showRetryButton = true
                }
            } else {
                showRetryButton = false
            }
        }

        Column(
            modifier = Modifier.fillMaxSize().padding(32.dp),
            verticalArrangement = Arrangement.Center,
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            if (!state.isSteamConnected) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    CircularProgressIndicator(modifier = Modifier.size(16.dp), strokeWidth = 2.dp)
                    Spacer(Modifier.width(8.dp))
                    Text("Connecting to Steam...", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.primary)
                }
                
                if (showRetryButton) {
                    TextButton(onClick = { 
                        showRetryButton = false
                        viewModel.retryConnection() 
                    }) {
                        Text("Retry Connection", style = MaterialTheme.typography.bodySmall)
                    }
                }
                Spacer(Modifier.height(16.dp))
            }

            OutlinedTextField(
                value = state.username,
                onValueChange = { viewModel.setUsername(it) },
                label = { Text("Username") },
                modifier = Modifier.fillMaxWidth(),
                enabled = !state.isLoggingIn
            )
            Spacer(Modifier.height(8.dp))
            OutlinedTextField(
                value = state.password,
                onValueChange = { viewModel.setPassword(it) },
                label = { Text("Password") },
                visualTransformation = if (passwordVisible) VisualTransformation.None else PasswordVisualTransformation(),
                trailingIcon = {
                    IconButton(onClick = onTogglePassword) {
                        Icon(if (passwordVisible) Icons.Filled.Visibility else Icons.Filled.VisibilityOff, null)
                    }
                },
                modifier = Modifier.fillMaxWidth(),
                enabled = !state.isLoggingIn
            )
            Spacer(Modifier.height(16.dp))

            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Checkbox(checked = state.rememberSession, onCheckedChange = { viewModel.setRememberSession(it) }, enabled = !state.isLoggingIn)
                Text("Remember Me", style = MaterialTheme.typography.bodyMedium)
            }

            Spacer(Modifier.height(24.dp))

            Button(
                onClick = { viewModel.onCredentialLogin() },
                modifier = Modifier.fillMaxWidth().height(50.dp),
                enabled = state.username.isNotEmpty() && state.password.isNotEmpty() && !state.isLoggingIn && state.isSteamConnected
            ) {
                if (state.isLoggingIn) {
                    CircularProgressIndicator(modifier = Modifier.size(24.dp), color = MaterialTheme.colorScheme.onPrimary)
                } else {
                    Text("Login")
                }
            }

            Spacer(Modifier.height(16.dp))

            TextButton(onClick = { viewModel.onShowLoginScreen(LoginScreen.QR) }, enabled = !state.isLoggingIn) {
                Text("Sign in with QR Code")
            }
            
            Spacer(Modifier.height(16.dp))
            TextButton(onClick = { finish() }) {
                Text("Cancel")
            }
        }
    }

    @Composable
    fun QrLogin(state: com.winlator.cmod.steam.ui.data.UserLoginState, viewModel: SteamLoginViewModel) {
        Column(
            modifier = Modifier.fillMaxSize().padding(32.dp),
            verticalArrangement = Arrangement.Center,
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text("Sign in with QR Code", style = MaterialTheme.typography.headlineSmall)
            Spacer(Modifier.height(16.dp))
            
            if (state.qrCode != null) {
                QrCodeImage(content = state.qrCode!!, size = 250.dp)
                Spacer(Modifier.height(24.dp))
                Text("Scan this QR code with the Steam mobile app to sign in.", style = MaterialTheme.typography.bodyMedium)
            } else if (state.isQrFailed) {
                Text("Failed to load QR code", color = MaterialTheme.colorScheme.error)
                Spacer(Modifier.height(16.dp))
                Button(onClick = { viewModel.onQrRetry() }) {
                    Text("Retry")
                }
            } else {
                CircularProgressIndicator()
            }
            
            Spacer(Modifier.height(24.dp))
            TextButton(onClick = { viewModel.onShowLoginScreen(LoginScreen.CREDENTIAL) }) {
                Text("Back to Credentials")
            }
        }
    }

    @Composable
    fun TwoFactorLogin(state: com.winlator.cmod.steam.ui.data.UserLoginState, viewModel: SteamLoginViewModel) {
        Column(
            modifier = Modifier.fillMaxSize().padding(32.dp),
            verticalArrangement = Arrangement.Center,
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            val methodText = when (state.lastTwoFactorMethod) {
                "steam_guard" -> "Confirm login in your Steam mobile app"
                "email_code" -> "Enter the code sent to your email (${state.email})"
                else -> "Enter your Steam Guard code"
            }
            
            Text("Two-Factor Authentication", style = MaterialTheme.typography.headlineSmall)
            Spacer(Modifier.height(16.dp))
            Text(methodText, style = MaterialTheme.typography.bodyMedium)
            
            if (state.lastTwoFactorMethod != "steam_guard") {
                Spacer(Modifier.height(16.dp))
                OutlinedTextField(
                    value = state.twoFactorCode,
                    onValueChange = { viewModel.setTwoFactorCode(it) },
                    label = { Text("Code") },
                    modifier = Modifier.fillMaxWidth(),
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                    enabled = !state.isLoggingIn
                )
                Spacer(Modifier.height(24.dp))
                Button(
                    onClick = { viewModel.submitTwoFactor() },
                    modifier = Modifier.fillMaxWidth().height(50.dp),
                    enabled = state.twoFactorCode.length >= 5 && !state.isLoggingIn
                ) {
                    Text("Submit")
                }
            } else {
                Spacer(Modifier.height(32.dp))
                CircularProgressIndicator()
                Spacer(Modifier.height(16.dp))
                Text("Waiting for confirmation...", style = MaterialTheme.typography.bodySmall)
            }
            
            Spacer(Modifier.height(24.dp))
            TextButton(onClick = { viewModel.onShowLoginScreen(LoginScreen.CREDENTIAL) }) {
                Text("Cancel")
            }
        }
    }
}
