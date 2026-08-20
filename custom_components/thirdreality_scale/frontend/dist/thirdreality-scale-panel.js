/**
 * @license
 * Copyright 2019 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const t=globalThis,e=t.ShadowRoot&&(void 0===t.ShadyCSS||t.ShadyCSS.nativeShadow)&&"adoptedStyleSheets"in Document.prototype&&"replace"in CSSStyleSheet.prototype,i=Symbol(),s=new WeakMap;let r=class{constructor(t,e,s){if(this._$cssResult$=!0,s!==i)throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText=t,this.t=e}get styleSheet(){let t=this.o;const i=this.t;if(e&&void 0===t){const e=void 0!==i&&1===i.length;e&&(t=s.get(i)),void 0===t&&((this.o=t=new CSSStyleSheet).replaceSync(this.cssText),e&&s.set(i,t))}return t}toString(){return this.cssText}};const o=(t,...e)=>{const s=1===t.length?t[0]:e.reduce((e,i,s)=>e+(t=>{if(!0===t._$cssResult$)return t.cssText;if("number"==typeof t)return t;throw Error("Value passed to 'css' function must be a 'css' function result: "+t+". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.")})(i)+t[s+1],t[0]);return new r(s,t,i)},a=e?t=>t:t=>t instanceof CSSStyleSheet?(t=>{let e="";for(const i of t.cssRules)e+=i.cssText;return(t=>new r("string"==typeof t?t:t+"",void 0,i))(e)})(t):t,{is:n,defineProperty:l,getOwnPropertyDescriptor:c,getOwnPropertyNames:d,getOwnPropertySymbols:h,getPrototypeOf:p}=Object,u=globalThis,_=u.trustedTypes,g=_?_.emptyScript:"",m=u.reactiveElementPolyfillSupport,v=(t,e)=>t,f={toAttribute(t,e){switch(e){case Boolean:t=t?g:null;break;case Object:case Array:t=null==t?t:JSON.stringify(t)}return t},fromAttribute(t,e){let i=t;switch(e){case Boolean:i=null!==t;break;case Number:i=null===t?null:Number(t);break;case Object:case Array:try{i=JSON.parse(t)}catch(t){i=null}}return i}},y=(t,e)=>!n(t,e),b={attribute:!0,type:String,converter:f,reflect:!1,useDefault:!1,hasChanged:y};
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */Symbol.metadata??=Symbol("metadata"),u.litPropertyMetadata??=new WeakMap;let x=class extends HTMLElement{static addInitializer(t){this._$Ei(),(this.l??=[]).push(t)}static get observedAttributes(){return this.finalize(),this._$Eh&&[...this._$Eh.keys()]}static createProperty(t,e=b){if(e.state&&(e.attribute=!1),this._$Ei(),this.prototype.hasOwnProperty(t)&&((e=Object.create(e)).wrapped=!0),this.elementProperties.set(t,e),!e.noAccessor){const i=Symbol(),s=this.getPropertyDescriptor(t,i,e);void 0!==s&&l(this.prototype,t,s)}}static getPropertyDescriptor(t,e,i){const{get:s,set:r}=c(this.prototype,t)??{get(){return this[e]},set(t){this[e]=t}};return{get:s,set(e){const o=s?.call(this);r?.call(this,e),this.requestUpdate(t,o,i)},configurable:!0,enumerable:!0}}static getPropertyOptions(t){return this.elementProperties.get(t)??b}static _$Ei(){if(this.hasOwnProperty(v("elementProperties")))return;const t=p(this);t.finalize(),void 0!==t.l&&(this.l=[...t.l]),this.elementProperties=new Map(t.elementProperties)}static finalize(){if(this.hasOwnProperty(v("finalized")))return;if(this.finalized=!0,this._$Ei(),this.hasOwnProperty(v("properties"))){const t=this.properties,e=[...d(t),...h(t)];for(const i of e)this.createProperty(i,t[i])}const t=this[Symbol.metadata];if(null!==t){const e=litPropertyMetadata.get(t);if(void 0!==e)for(const[t,i]of e)this.elementProperties.set(t,i)}this._$Eh=new Map;for(const[t,e]of this.elementProperties){const i=this._$Eu(t,e);void 0!==i&&this._$Eh.set(i,t)}this.elementStyles=this.finalizeStyles(this.styles)}static finalizeStyles(t){const e=[];if(Array.isArray(t)){const i=new Set(t.flat(1/0).reverse());for(const t of i)e.unshift(a(t))}else void 0!==t&&e.push(a(t));return e}static _$Eu(t,e){const i=e.attribute;return!1===i?void 0:"string"==typeof i?i:"string"==typeof t?t.toLowerCase():void 0}constructor(){super(),this._$Ep=void 0,this.isUpdatePending=!1,this.hasUpdated=!1,this._$Em=null,this._$Ev()}_$Ev(){this._$ES=new Promise(t=>this.enableUpdating=t),this._$AL=new Map,this._$E_(),this.requestUpdate(),this.constructor.l?.forEach(t=>t(this))}addController(t){(this._$EO??=new Set).add(t),void 0!==this.renderRoot&&this.isConnected&&t.hostConnected?.()}removeController(t){this._$EO?.delete(t)}_$E_(){const t=new Map,e=this.constructor.elementProperties;for(const i of e.keys())this.hasOwnProperty(i)&&(t.set(i,this[i]),delete this[i]);t.size>0&&(this._$Ep=t)}createRenderRoot(){const i=this.shadowRoot??this.attachShadow(this.constructor.shadowRootOptions);return((i,s)=>{if(e)i.adoptedStyleSheets=s.map(t=>t instanceof CSSStyleSheet?t:t.styleSheet);else for(const e of s){const s=document.createElement("style"),r=t.litNonce;void 0!==r&&s.setAttribute("nonce",r),s.textContent=e.cssText,i.appendChild(s)}})(i,this.constructor.elementStyles),i}connectedCallback(){this.renderRoot??=this.createRenderRoot(),this.enableUpdating(!0),this._$EO?.forEach(t=>t.hostConnected?.())}enableUpdating(t){}disconnectedCallback(){this._$EO?.forEach(t=>t.hostDisconnected?.())}attributeChangedCallback(t,e,i){this._$AK(t,i)}_$ET(t,e){const i=this.constructor.elementProperties.get(t),s=this.constructor._$Eu(t,i);if(void 0!==s&&!0===i.reflect){const r=(void 0!==i.converter?.toAttribute?i.converter:f).toAttribute(e,i.type);this._$Em=t,null==r?this.removeAttribute(s):this.setAttribute(s,r),this._$Em=null}}_$AK(t,e){const i=this.constructor,s=i._$Eh.get(t);if(void 0!==s&&this._$Em!==s){const t=i.getPropertyOptions(s),r="function"==typeof t.converter?{fromAttribute:t.converter}:void 0!==t.converter?.fromAttribute?t.converter:f;this._$Em=s;const o=r.fromAttribute(e,t.type);this[s]=o??this._$Ej?.get(s)??o,this._$Em=null}}requestUpdate(t,e,i,s=!1,r){if(void 0!==t){const o=this.constructor;if(!1===s&&(r=this[t]),i??=o.getPropertyOptions(t),!((i.hasChanged??y)(r,e)||i.useDefault&&i.reflect&&r===this._$Ej?.get(t)&&!this.hasAttribute(o._$Eu(t,i))))return;this.C(t,e,i)}!1===this.isUpdatePending&&(this._$ES=this._$EP())}C(t,e,{useDefault:i,reflect:s,wrapped:r},o){i&&!(this._$Ej??=new Map).has(t)&&(this._$Ej.set(t,o??e??this[t]),!0!==r||void 0!==o)||(this._$AL.has(t)||(this.hasUpdated||i||(e=void 0),this._$AL.set(t,e)),!0===s&&this._$Em!==t&&(this._$Eq??=new Set).add(t))}async _$EP(){this.isUpdatePending=!0;try{await this._$ES}catch(t){Promise.reject(t)}const t=this.scheduleUpdate();return null!=t&&await t,!this.isUpdatePending}scheduleUpdate(){return this.performUpdate()}performUpdate(){if(!this.isUpdatePending)return;if(!this.hasUpdated){if(this.renderRoot??=this.createRenderRoot(),this._$Ep){for(const[t,e]of this._$Ep)this[t]=e;this._$Ep=void 0}const t=this.constructor.elementProperties;if(t.size>0)for(const[e,i]of t){const{wrapped:t}=i,s=this[e];!0!==t||this._$AL.has(e)||void 0===s||this.C(e,void 0,i,s)}}let t=!1;const e=this._$AL;try{t=this.shouldUpdate(e),t?(this.willUpdate(e),this._$EO?.forEach(t=>t.hostUpdate?.()),this.update(e)):this._$EM()}catch(e){throw t=!1,this._$EM(),e}t&&this._$AE(e)}willUpdate(t){}_$AE(t){this._$EO?.forEach(t=>t.hostUpdated?.()),this.hasUpdated||(this.hasUpdated=!0,this.firstUpdated(t)),this.updated(t)}_$EM(){this._$AL=new Map,this.isUpdatePending=!1}get updateComplete(){return this.getUpdateComplete()}getUpdateComplete(){return this._$ES}shouldUpdate(t){return!0}update(t){this._$Eq&&=this._$Eq.forEach(t=>this._$ET(t,this[t])),this._$EM()}updated(t){}firstUpdated(t){}};x.elementStyles=[],x.shadowRootOptions={mode:"open"},x[v("elementProperties")]=new Map,x[v("finalized")]=new Map,m?.({ReactiveElement:x}),(u.reactiveElementVersions??=[]).push("2.1.2");
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const $=globalThis,S=t=>t,w=$.trustedTypes,k=w?w.createPolicy("lit-html",{createHTML:t=>t}):void 0,A="$lit$",C=`lit$${Math.random().toFixed(9).slice(2)}$`,E="?"+C,T=`<${E}>`,M=document,z=()=>M.createComment(""),R=t=>null===t||"object"!=typeof t&&"function"!=typeof t,O=Array.isArray,D="[ \t\n\f\r]",P=/<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g,F=/-->/g,H=/>/g,U=RegExp(`>|${D}(?:([^\\s"'>=/]+)(${D}*=${D}*(?:[^ \t\n\f\r"'\`<>=]|("|')|))|$)`,"g"),I=/'/g,N=/"/g,j=/^(?:script|style|textarea|title)$/i,q=(t=>(e,...i)=>({_$litType$:t,strings:e,values:i}))(1),L=Symbol.for("lit-noChange"),B=Symbol.for("lit-nothing"),W=new WeakMap,V=M.createTreeWalker(M,129);function J(t,e){if(!O(t)||!t.hasOwnProperty("raw"))throw Error("invalid template strings array");return void 0!==k?k.createHTML(e):e}const Y=(t,e)=>{const i=t.length-1,s=[];let r,o=2===e?"<svg>":3===e?"<math>":"",a=P;for(let e=0;e<i;e++){const i=t[e];let n,l,c=-1,d=0;for(;d<i.length&&(a.lastIndex=d,l=a.exec(i),null!==l);)d=a.lastIndex,a===P?"!--"===l[1]?a=F:void 0!==l[1]?a=H:void 0!==l[2]?(j.test(l[2])&&(r=RegExp("</"+l[2],"g")),a=U):void 0!==l[3]&&(a=U):a===U?">"===l[0]?(a=r??P,c=-1):void 0===l[1]?c=-2:(c=a.lastIndex-l[2].length,n=l[1],a=void 0===l[3]?U:'"'===l[3]?N:I):a===N||a===I?a=U:a===F||a===H?a=P:(a=U,r=void 0);const h=a===U&&t[e+1].startsWith("/>")?" ":"";o+=a===P?i+T:c>=0?(s.push(n),i.slice(0,c)+A+i.slice(c)+C+h):i+C+(-2===c?e:h)}return[J(t,o+(t[i]||"<?>")+(2===e?"</svg>":3===e?"</math>":"")),s]};class G{constructor({strings:t,_$litType$:e},i){let s;this.parts=[];let r=0,o=0;const a=t.length-1,n=this.parts,[l,c]=Y(t,e);if(this.el=G.createElement(l,i),V.currentNode=this.el.content,2===e||3===e){const t=this.el.content.firstChild;t.replaceWith(...t.childNodes)}for(;null!==(s=V.nextNode())&&n.length<a;){if(1===s.nodeType){if(s.hasAttributes())for(const t of s.getAttributeNames())if(t.endsWith(A)){const e=c[o++],i=s.getAttribute(t).split(C),a=/([.?@])?(.*)/.exec(e);n.push({type:1,index:r,name:a[2],strings:i,ctor:"."===a[1]?tt:"?"===a[1]?et:"@"===a[1]?it:X}),s.removeAttribute(t)}else t.startsWith(C)&&(n.push({type:6,index:r}),s.removeAttribute(t));if(j.test(s.tagName)){const t=s.textContent.split(C),e=t.length-1;if(e>0){s.textContent=w?w.emptyScript:"";for(let i=0;i<e;i++)s.append(t[i],z()),V.nextNode(),n.push({type:2,index:++r});s.append(t[e],z())}}}else if(8===s.nodeType)if(s.data===E)n.push({type:2,index:r});else{let t=-1;for(;-1!==(t=s.data.indexOf(C,t+1));)n.push({type:7,index:r}),t+=C.length-1}r++}}static createElement(t,e){const i=M.createElement("template");return i.innerHTML=t,i}}function K(t,e,i=t,s){if(e===L)return e;let r=void 0!==s?i._$Co?.[s]:i._$Cl;const o=R(e)?void 0:e._$litDirective$;return r?.constructor!==o&&(r?._$AO?.(!1),void 0===o?r=void 0:(r=new o(t),r._$AT(t,i,s)),void 0!==s?(i._$Co??=[])[s]=r:i._$Cl=r),void 0!==r&&(e=K(t,r._$AS(t,e.values),r,s)),e}class Q{constructor(t,e){this._$AV=[],this._$AN=void 0,this._$AD=t,this._$AM=e}get parentNode(){return this._$AM.parentNode}get _$AU(){return this._$AM._$AU}u(t){const{el:{content:e},parts:i}=this._$AD,s=(t?.creationScope??M).importNode(e,!0);V.currentNode=s;let r=V.nextNode(),o=0,a=0,n=i[0];for(;void 0!==n;){if(o===n.index){let e;2===n.type?e=new Z(r,r.nextSibling,this,t):1===n.type?e=new n.ctor(r,n.name,n.strings,this,t):6===n.type&&(e=new st(r,this,t)),this._$AV.push(e),n=i[++a]}o!==n?.index&&(r=V.nextNode(),o++)}return V.currentNode=M,s}p(t){let e=0;for(const i of this._$AV)void 0!==i&&(void 0!==i.strings?(i._$AI(t,i,e),e+=i.strings.length-2):i._$AI(t[e])),e++}}class Z{get _$AU(){return this._$AM?._$AU??this._$Cv}constructor(t,e,i,s){this.type=2,this._$AH=B,this._$AN=void 0,this._$AA=t,this._$AB=e,this._$AM=i,this.options=s,this._$Cv=s?.isConnected??!0}get parentNode(){let t=this._$AA.parentNode;const e=this._$AM;return void 0!==e&&11===t?.nodeType&&(t=e.parentNode),t}get startNode(){return this._$AA}get endNode(){return this._$AB}_$AI(t,e=this){t=K(this,t,e),R(t)?t===B||null==t||""===t?(this._$AH!==B&&this._$AR(),this._$AH=B):t!==this._$AH&&t!==L&&this._(t):void 0!==t._$litType$?this.$(t):void 0!==t.nodeType?this.T(t):(t=>O(t)||"function"==typeof t?.[Symbol.iterator])(t)?this.k(t):this._(t)}O(t){return this._$AA.parentNode.insertBefore(t,this._$AB)}T(t){this._$AH!==t&&(this._$AR(),this._$AH=this.O(t))}_(t){this._$AH!==B&&R(this._$AH)?this._$AA.nextSibling.data=t:this.T(M.createTextNode(t)),this._$AH=t}$(t){const{values:e,_$litType$:i}=t,s="number"==typeof i?this._$AC(t):(void 0===i.el&&(i.el=G.createElement(J(i.h,i.h[0]),this.options)),i);if(this._$AH?._$AD===s)this._$AH.p(e);else{const t=new Q(s,this),i=t.u(this.options);t.p(e),this.T(i),this._$AH=t}}_$AC(t){let e=W.get(t.strings);return void 0===e&&W.set(t.strings,e=new G(t)),e}k(t){O(this._$AH)||(this._$AH=[],this._$AR());const e=this._$AH;let i,s=0;for(const r of t)s===e.length?e.push(i=new Z(this.O(z()),this.O(z()),this,this.options)):i=e[s],i._$AI(r),s++;s<e.length&&(this._$AR(i&&i._$AB.nextSibling,s),e.length=s)}_$AR(t=this._$AA.nextSibling,e){for(this._$AP?.(!1,!0,e);t!==this._$AB;){const e=S(t).nextSibling;S(t).remove(),t=e}}setConnected(t){void 0===this._$AM&&(this._$Cv=t,this._$AP?.(t))}}class X{get tagName(){return this.element.tagName}get _$AU(){return this._$AM._$AU}constructor(t,e,i,s,r){this.type=1,this._$AH=B,this._$AN=void 0,this.element=t,this.name=e,this._$AM=s,this.options=r,i.length>2||""!==i[0]||""!==i[1]?(this._$AH=Array(i.length-1).fill(new String),this.strings=i):this._$AH=B}_$AI(t,e=this,i,s){const r=this.strings;let o=!1;if(void 0===r)t=K(this,t,e,0),o=!R(t)||t!==this._$AH&&t!==L,o&&(this._$AH=t);else{const s=t;let a,n;for(t=r[0],a=0;a<r.length-1;a++)n=K(this,s[i+a],e,a),n===L&&(n=this._$AH[a]),o||=!R(n)||n!==this._$AH[a],n===B?t=B:t!==B&&(t+=(n??"")+r[a+1]),this._$AH[a]=n}o&&!s&&this.j(t)}j(t){t===B?this.element.removeAttribute(this.name):this.element.setAttribute(this.name,t??"")}}class tt extends X{constructor(){super(...arguments),this.type=3}j(t){this.element[this.name]=t===B?void 0:t}}class et extends X{constructor(){super(...arguments),this.type=4}j(t){this.element.toggleAttribute(this.name,!!t&&t!==B)}}class it extends X{constructor(t,e,i,s,r){super(t,e,i,s,r),this.type=5}_$AI(t,e=this){if((t=K(this,t,e,0)??B)===L)return;const i=this._$AH,s=t===B&&i!==B||t.capture!==i.capture||t.once!==i.once||t.passive!==i.passive,r=t!==B&&(i===B||s);s&&this.element.removeEventListener(this.name,this,i),r&&this.element.addEventListener(this.name,this,t),this._$AH=t}handleEvent(t){"function"==typeof this._$AH?this._$AH.call(this.options?.host??this.element,t):this._$AH.handleEvent(t)}}class st{constructor(t,e,i){this.element=t,this.type=6,this._$AN=void 0,this._$AM=e,this.options=i}get _$AU(){return this._$AM._$AU}_$AI(t){K(this,t)}}const rt=$.litHtmlPolyfillSupport;rt?.(G,Z),($.litHtmlVersions??=[]).push("3.3.3");const ot=globalThis;
/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */class at extends x{constructor(){super(...arguments),this.renderOptions={host:this},this._$Do=void 0}createRenderRoot(){const t=super.createRenderRoot();return this.renderOptions.renderBefore??=t.firstChild,t}update(t){const e=this.render();this.hasUpdated||(this.renderOptions.isConnected=this.isConnected),super.update(t),this._$Do=((t,e,i)=>{const s=i?.renderBefore??e;let r=s._$litPart$;if(void 0===r){const t=i?.renderBefore??null;s._$litPart$=r=new Z(e.insertBefore(z(),t),t,void 0,i??{})}return r._$AI(t),r})(e,this.renderRoot,this.renderOptions)}connectedCallback(){super.connectedCallback(),this._$Do?.setConnected(!0)}disconnectedCallback(){super.disconnectedCallback(),this._$Do?.setConnected(!1)}render(){return L}}at._$litElement$=!0,at.finalized=!0,ot.litElementHydrateSupport?.({LitElement:at});const nt=ot.litElementPolyfillSupport;nt?.({LitElement:at}),(ot.litElementVersions??=[]).push("4.2.2");customElements.define("thirdreality-scale-panel",class extends at{static get properties(){return{hass:{type:Object},narrow:{type:Boolean},route:{type:Object},panel:{type:Object},_activeTab:{type:String},_foodSearch:{type:String},_confirmReset:{type:Boolean},_unit:{type:String}}}constructor(){super(),this._activeTab="cocktail",this._foodSearch=null,this._confirmReset=!1,this._unit=localStorage.getItem("tr_scale_unit")||"g"}_toggleUnit(){this._unit="g"===this._unit?"oz":"g",localStorage.setItem("tr_scale_unit",this._unit)}_displayWeight(t){return"oz"===this._unit?`${(t/28.35).toFixed(1)}`:`${Math.round(t)}`}_unitLabel(){return this._unit}static get styles(){return o`
      :host { display: block; height: 100%; font-family: var(--paper-font-body1_-_font-family, Roboto, sans-serif); }
      * { box-sizing: border-box; }

      .panel { height: 100%; display: flex; flex-direction: column; background: var(--primary-background-color, #fafafa); }

      /* Header */
      .header { padding: 16px 24px 0; background: var(--card-background-color, white); }
      .header h1 { margin: 0 0 16px; font-size: 24px; font-weight: 400; color: var(--primary-text-color); }
      .tabs { display: flex; gap: 24px; border-bottom: 1px solid var(--divider-color, #e0e0e0); }
      .tab {
        padding: 8px 0 12px; cursor: pointer; font-size: 14px; font-weight: 500;
        color: var(--secondary-text-color); border-bottom: 2px solid transparent;
        transition: all 0.2s; user-select: none;
      }
      .tab:hover { color: var(--primary-text-color); }
      .tab.active { color: var(--primary-color); border-bottom-color: var(--primary-color); }

      /* Content */
      .content { flex: 1; overflow-y: auto; padding: 24px; }
      .content::-webkit-scrollbar { width: 4px; }
      .content::-webkit-scrollbar-thumb { background: rgba(0,0,0,0.1); border-radius: 2px; }

      /* Section */
      .section {
        background: var(--card-background-color, white);
        border: 1px solid var(--divider-color, #e8e8e8);
        border-radius: 8px; padding: 20px; margin-bottom: 16px;
      }
      .section-title { font-size: 16px; font-weight: 500; color: var(--primary-text-color); margin: 0 0 16px; }
      .section-desc { font-size: 14px; color: var(--secondary-text-color); margin: 0 0 16px; }

      /* Form elements */
      .form-row { display: flex; align-items: center; gap: 12px; margin-bottom: 12px; }
      .form-label { font-size: 13px; color: var(--secondary-text-color); margin-bottom: 4px; }
      .form-select, .form-input {
        width: 100%; padding: 10px 12px; font-size: 14px;
        border: 1px solid var(--divider-color, #ddd); border-radius: 6px;
        background: var(--card-background-color, white); color: var(--primary-text-color);
        outline: none; transition: border-color 0.2s;
      }
      .form-select:focus, .form-input:focus { border-color: var(--primary-color); }
      .form-input::placeholder { color: var(--disabled-text-color, #999); }

      /* Buttons */
      .btn-group { display: flex; gap: 8px; margin-top: 12px; }
      .btn {
        padding: 10px 16px; border-radius: 6px; font-size: 13px; font-weight: 500;
        cursor: pointer; transition: all 0.15s; border: 1px solid transparent;
        display: inline-flex; align-items: center; gap: 4px;
      }
      .btn:active { transform: scale(0.97); }
      .btn-filled { background: var(--primary-color); color: white; border-color: var(--primary-color); }
      .btn-filled:hover { opacity: 0.9; }
      .btn-outline { background: transparent; color: var(--primary-color); border-color: var(--primary-color); }
      .btn-outline:hover { background: rgba(3,169,244,0.05); }
      .btn-success { background: #4caf50; color: white; border-color: #4caf50; }
      .btn-danger { background: transparent; color: #f44336; border-color: #f44336; }
      .btn-danger:hover { background: rgba(244,67,54,0.05); }
      .btn-ghost { background: transparent; color: var(--secondary-text-color); border-color: var(--divider-color); }

      /* Weight inline */
      .weight-inline { display: flex; align-items: baseline; justify-content: center; padding: 8px 0; }
      .weight-num { font-size: 28px; font-weight: 300; color: var(--primary-text-color); }
      .weight-unit { font-size: 14px; color: var(--secondary-text-color); margin-left: 4px; }

      /* Progress ring */
      .progress-section { display: flex; align-items: center; gap: 20px; }
      .progress-ring { position: relative; width: 80px; height: 80px; flex-shrink: 0; }
      .progress-ring svg { transform: rotate(-90deg); }
      .progress-ring .bg { fill: none; stroke: var(--divider-color, #e0e0e0); stroke-width: 6; }
      .progress-ring .fill { fill: none; stroke-width: 6; stroke-linecap: round; transition: stroke-dashoffset 0.5s; }
      .progress-ring .center-text {
        position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
        font-size: 16px; font-weight: 500; color: var(--primary-text-color);
      }
      .progress-info { flex: 1; }
      .progress-info .main { font-size: 20px; font-weight: 400; color: var(--primary-text-color); margin-bottom: 4px; }
      .progress-info .sub { font-size: 13px; color: var(--secondary-text-color); }

      /* Progress + History layout */
      .calories-top { display: flex; gap: 12px; align-items: center; }
      .calories-top-left { flex: 0 0 auto; }
      .calories-top-center { flex: 0 0 auto; display: flex; flex-direction: column; align-items: center; gap: 8px; padding: 0 8px; }
      .calories-top-right { flex: 1; display: flex; flex-direction: column; justify-content: center; }
      .mini-history-title { font-size: 11px; font-weight: 500; color: var(--secondary-text-color); margin-bottom: 8px; text-align: center; }
      .mini-history-chart { display: flex; align-items: flex-end; justify-content: center; gap: 4px; height: 60px; }
      .mini-history-col { display: flex; flex-direction: column; align-items: center; gap: 2px; flex: 1; max-width: 36px; }
      .mini-history-bar-v { width: 100%; min-width: 12px; border-radius: 3px 3px 0 0; transition: height 0.3s; }
      .mini-history-label { font-size: 9px; color: var(--secondary-text-color); }

      /* Status */
      .status-msg {
        padding: 10px 14px; background: var(--secondary-background-color, #f5f5f5);
        border-radius: 6px; font-size: 13px; color: var(--primary-text-color); margin-bottom: 12px;
      }

      /* List */
      .list-item {
        display: flex; align-items: center; padding: 10px 0;
        border-bottom: 1px solid var(--divider-color, #eee); font-size: 14px;
      }
      .list-item:last-child { border-bottom: none; }
      .list-num {
        width: 22px; height: 22px; border-radius: 50%; background: var(--primary-color);
        color: white; display: flex; align-items: center; justify-content: center;
        font-size: 11px; font-weight: 600; margin-right: 12px; flex-shrink: 0;
      }
      .list-item.active { background: rgba(3,169,244,0.05); margin: 0 -20px; padding: 10px 20px; border-radius: 4px; }

      /* Meal log */
      .log-item { font-size: 13px; color: var(--secondary-text-color); padding: 6px 0; border-bottom: 1px solid var(--divider-color, #f0f0f0); }
      .log-item:last-child { border-bottom: none; }

      /* Settings row */
      .setting-row { display: flex; align-items: center; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid var(--divider-color, #eee); }
      .setting-row:last-child { border-bottom: none; }
      .setting-label { font-size: 14px; color: var(--primary-text-color); }
      .setting-value { font-size: 14px; color: var(--primary-color); font-weight: 500; }

      /* Compact settings inputs */
      .settings-compact { display: flex; gap: 12px; }
      .settings-compact > div { flex: 1; }
      .settings-compact label { display: block; font-size: 12px; color: var(--secondary-text-color); margin-bottom: 4px; }
      .settings-compact input {
        width: 100%; padding: 8px 10px; border: 1px solid var(--divider-color, #ddd);
        border-radius: 6px; font-size: 14px; color: var(--primary-text-color);
        background: var(--card-background-color); outline: none;
      }
      .settings-compact input:focus { border-color: var(--primary-color); }

      /* History styles */
      .history-day {
        margin-bottom: 16px; padding-bottom: 16px;
        border-bottom: 1px solid var(--divider-color, #eee);
      }
      .history-day:last-child { border-bottom: none; margin-bottom: 0; padding-bottom: 0; }
      .history-day-header {
        display: flex; justify-content: space-between; align-items: center;
        margin-bottom: 8px;
      }
      .history-date { font-size: 14px; font-weight: 500; color: var(--primary-text-color); }
      .history-total {
        font-size: 13px; font-weight: 600; padding: 2px 8px;
        border-radius: 12px; background: var(--primary-color); color: white;
      }
      .history-meal {
        display: flex; align-items: center; gap: 8px;
        padding: 4px 0; font-size: 13px; color: var(--secondary-text-color);
      }
      .history-meal-time { 
        font-weight: 500; color: var(--primary-text-color); min-width: 45px;
      }
      .history-meal-cal { font-weight: 500; color: var(--primary-color); }
      .history-bar {
        height: 6px; border-radius: 3px; margin-top: 6px;
        background: var(--divider-color, #e0e0e0); overflow: hidden;
      }
      .history-bar-fill {
        height: 100%; border-radius: 3px; transition: width 0.3s;
      }
      .history-empty {
        text-align: center; padding: 40px 20px; color: var(--secondary-text-color); font-size: 14px;
      }

      @media (max-width: 768px) {
        .content { padding: 16px; }
        .header { padding: 12px 16px 0; }
        .form-row { flex-direction: column; align-items: stretch; }
        .btn-group { flex-wrap: wrap; }
        .progress-section { flex-direction: column; align-items: center; text-align: center; }
        .calories-top { flex-wrap: wrap; }
        .calories-top-left { flex: 1 1 100%; margin-bottom: 12px; }
        .calories-top-right { flex: 1 1 55%; }
        .calories-top-center { flex: 1 1 40%; border-left: none !important; padding-left: 0 !important; border-top: none; flex-direction: row; justify-content: space-around; gap: 16px; }
      }
    `}render(){return q`
      <div class="panel">
        <div class="header">
          <h1>Smart Scale</h1>
          <div class="tabs">
            <div class="tab ${"cocktail"===this._activeTab?"active":""}" @click=${()=>this._activeTab="cocktail"}>Cocktail</div>
            <div class="tab ${"calorie"===this._activeTab?"active":""}" @click=${()=>this._activeTab="calorie"}>Calories</div>
            <div class="tab ${"recipes"===this._activeTab?"active":""}" @click=${()=>this._activeTab="recipes"}>Recipes</div>
            <div class="tab ${"foods"===this._activeTab?"active":""}" @click=${()=>this._activeTab="foods"}>Foods</div>
          </div>
        </div>
        <div class="content">
          ${"cocktail"===this._activeTab?this._renderCocktail():"calorie"===this._activeTab?this._renderCalorie():"recipes"===this._activeTab?this._renderRecipes():this._renderFoods()}
        </div>
      </div>
    `}_renderCocktail(){const t=this._getState("select.thirdreality_smart_scale_cocktail_step");return"mixing"===t?this._renderMixing():"complete"===t?this._renderComplete():this._renderCocktailIdle()}_renderCocktailIdle(){const t=this._getState("select.thirdreality_smart_scale_select_cocktail"),e=this._getOptions("select.thirdreality_smart_scale_select_cocktail"),i=this._getState("text.thirdreality_smart_scale_custom_recipe");return q`
      <div class="section">
        <h3 class="section-title">Select Recipe</h3>
        <p class="section-desc">Choose a cocktail recipe and press start to begin guided mixing.</p>
        <select class="form-select" @change=${this._onCocktailSelect}>
          ${e.map(e=>q`<option value=${e} ?selected=${e===t}>${e}</option>`)}
        </select>
        ${"custom"===t?q`
          <div style="margin-top:12px">
            <div class="form-label">Custom recipe (format: ingredient:weight,...)</div>
            <input class="form-input" .value=${i||""} placeholder="vodka:50,orange juice:100" @change=${this._onCustomRecipeChange} />
          </div>
        `:""}
        <div class="btn-group">
          <button class="btn btn-filled" @click=${this._startCocktail}>Start Mixing</button>
        </div>
      </div>
    `}_renderRecipePreview(t){const e=this._getState("text.thirdreality_smart_scale_cocktail_recipes_database");if(!e)return"";let i="";for(const s of e.split("|")){const e=s.split("=");if(2===e.length&&e[0].trim()===t){i=e[1].trim();break}}if(!i)return"";const s=i.split(",").map(t=>t.trim()).filter(t=>t);return q`
      <div style="margin-top:12px;padding:12px;background:var(--secondary-background-color,#f9f9f9);border-radius:6px">
        <div style="font-size:12px;color:var(--secondary-text-color);margin-bottom:8px;font-weight:500">Recipe Preview:</div>
        ${s.map(t=>{const e=t.split(":");return q`<div style="font-size:13px;color:var(--primary-text-color);padding:2px 0">${e[0]}${e[1]?` — ${e[1]}g`:""}</div>`})}
      </div>
    `}_renderMixing(){const t=this._getState("text.thirdreality_smart_scale_cocktail_status"),e=this._getState("text.thirdreality_smart_scale_cocktail_recipe_list"),i=this._getState("sensor.thirdreality_smart_scale_weight")||"0",s=e?e.split(" | ").filter(t=>t.trim()):[];return q`
      ${t?q`<div class="status-msg">${t}</div>`:""}
      <div class="section">
        <div class="weight-inline">
          <span class="weight-num">${this._displayWeight(parseFloat(i))}</span>
          <span class="weight-unit">${this._unitLabel()}</span>
          <span @click=${this._toggleUnit} style="margin-left:8px;padding:2px 8px;font-size:11px;border-radius:10px;cursor:pointer;background:var(--secondary-background-color,#eee);color:var(--secondary-text-color);border:1px solid var(--divider-color,#ddd)">${"g"===this._unit?"→oz":"→g"}</span>
        </div>
      </div>
      ${s.length?q`
        <div class="section">
          <h3 class="section-title">Ingredients</h3>
          ${s.map((t,e)=>q`
            <div class="list-item"><span class="list-num">${e+1}</span><span>${t.replace(/^\d+\.\s*/,"")}</span></div>
          `)}
        </div>
      `:""}
      <div class="btn-group">
        <button class="btn btn-success" @click=${this._doneCocktail}>Done — Next Step</button>
        <button class="btn btn-ghost" @click=${this._backToIdle}>Back</button>
      </div>
    `}_renderComplete(){return q`
      <div class="section" style="text-align:center;padding:40px 20px">
        <h3 class="section-title" style="font-size:20px">Cheers! Your cocktail is ready.</h3>
        <p class="section-desc">All ingredients have been added. Enjoy!</p>
        <div class="btn-group" style="justify-content:center">
          <button class="btn btn-outline" @click=${this._backToIdle}>Make Another</button>
        </div>
      </div>
    `}_renderCalorie(){const t=parseFloat(this._getState("sensor.thirdreality_smart_scale_weight"))||0,e=parseFloat(this._getState("number.thirdreality_smart_scale_today_calories"))||0,i=parseFloat(this._getState("number.thirdreality_smart_scale_meal_calories"))||0,s=parseFloat(this._getState("number.thirdreality_smart_scale_daily_calorie_target"))||2e3,r=this._getState("select.thirdreality_smart_scale_food_preset"),o=this._getOptions("select.thirdreality_smart_scale_food_preset"),a=this._getState("text.thirdreality_smart_scale_calorie_status"),n=this._getState("text.thirdreality_smart_scale_meal_log"),l=this._getState("text.thirdreality_smart_scale_custom_food_name"),c=this._getState("number.thirdreality_smart_scale_custom_cal_per_100g"),d=s>0?Math.min(Math.round(e/s*100),100):0,h=Math.round(s-e),p=2*Math.PI*34;return q`
      <!-- Progress + History side by side -->
      <div class="section">
        <div class="calories-top">
          <div class="calories-top-left">
            <div class="progress-section">
              <div class="progress-ring">
                <svg width="80" height="80" viewBox="0 0 80 80">
                  <circle class="bg" cx="40" cy="40" r="34"></circle>
                  <circle class="fill" cx="40" cy="40" r="34" stroke="${d>=100?"#f44336":d>=75?"#ff9800":"#4caf50"}"
                    stroke-dasharray="${p}" stroke-dashoffset="${p-d/100*p}"></circle>
                </svg>
                <span class="center-text">${d}%</span>
              </div>
              <div class="progress-info">
                <div class="main">${Math.round(e)} / ${Math.round(s)} kcal</div>
                <div class="sub">${h>0?`${h} kcal remaining`:`Exceeded by ${Math.abs(h)} kcal`}</div>
              </div>
            </div>
          </div>
          <div class="calories-top-right" style="flex:1">
            ${this._renderMiniHistory(s)}
          </div>
          <div class="calories-top-center" style="border-left:1px solid var(--divider-color,#eee);padding-left:14px;min-width:100px">
            <div style="margin-bottom:6px">
              <div style="font-size:10px;color:var(--secondary-text-color);margin-bottom:2px">Current Streak</div>
              <div style="font-size:16px;font-weight:500;color:var(--primary-text-color)">${this._getStreak()} days</div>
            </div>
            <div style="margin-bottom:6px">
              <div style="font-size:10px;color:var(--secondary-text-color);margin-bottom:2px">Best Streak</div>
              <div style="font-size:16px;font-weight:500;color:var(--primary-text-color)">${this._getBestStreak()} days</div>
            </div>
            <div>
              <div style="font-size:10px;color:var(--secondary-text-color);margin-bottom:2px">Weekly Avg</div>
              <div style="font-size:16px;font-weight:500;color:var(--primary-text-color)">${this._getWeekAvg()} kcal</div>
            </div>
          </div>
        </div>
        <!-- Motivation text - prominent, left-aligned -->
        <div style="margin-top:14px;padding-top:12px;border-top:1px solid var(--divider-color,#eee);font-size:15px;font-weight:400;color:var(--primary-text-color)">
          ${this._getMotivation(d)}
        </div>
      </div>

      <!-- Today's Meals -->
      ${this._renderTodayMeals()}

      <!-- Daily Goals -->
      <div class="section">
        <h3 class="section-title">Daily Goals</h3>
        <div class="settings-compact">
          <div>
            <label>Daily Target (kcal)</label>
            <input type="number" .value=${s} @change=${this._onDailyTargetChange} />
          </div>
          <div>
            <label>Meal Warning (kcal)</label>
            <input type="number" .value=${parseFloat(this._getState("number.thirdreality_smart_scale_meal_calorie_warning"))||800} @change=${this._onMealWarningChange} />
          </div>
        </div>
      </div>

      <!-- Add Food -->
      <div class="section">
        <h3 class="section-title">Add Food</h3>
        ${this._renderQuickAdd(o)}
        <div style="position:relative;margin-bottom:8px">
          <input class="form-input" placeholder="Search food..." 
            .value=${null!==this._foodSearch?this._foodSearch:r||""}
            @input=${this._onFoodSearchInput}
            @focus=${()=>{null===this._foodSearch&&(this._foodSearch=""),this.requestUpdate()}}
            @blur=${()=>{setTimeout(()=>{this._foodSearch=null,this.requestUpdate()},200)}}
          />
          ${null!==this._foodSearch&&void 0!==this._foodSearch?q`
            <div style="position:absolute;top:100%;left:0;right:0;z-index:10;max-height:200px;overflow-y:auto;
              background:var(--card-background-color,white);border:1px solid var(--divider-color,#ddd);
              border-radius:0 0 6px 6px;box-shadow:0 4px 12px rgba(0,0,0,0.1)">
              ${this._filterFood(o).slice(0,8).map(t=>q`
                <div @click=${()=>this._selectFoodFromSearch(t)}
                  style="padding:10px 12px;font-size:14px;cursor:pointer;
                  border-bottom:1px solid var(--divider-color,#f0f0f0);
                  color:var(--primary-text-color);
                  background:${t===r?"var(--secondary-background-color,#f5f5f5)":"transparent"}"
                >${t}</div>
              `)}
              ${0===this._filterFood(o).length?q`
                <div style="padding:10px 12px;font-size:13px;color:var(--secondary-text-color)">Not found — add it in Foods tab</div>
              `:""}
            </div>
          `:""}
        </div>
        <div style="margin-top:12px">
          <div class="form-label">One-time food (not saved):</div>
          <div style="display:flex;gap:8px">
            <input class="form-input" placeholder="Food name" .value=${l||""} @change=${this._onCustomFoodNameChange} style="flex:2" />
            <input class="form-input" type="number" placeholder="Cal/100g" .value=${c&&"0"!==c?c:""} @change=${this._onCustomCalChange} style="flex:1" />
          </div>
        </div>
        <div class="weight-inline">
          <span class="weight-num">${this._displayWeight(t)}</span>
          <span class="weight-unit">${this._unitLabel()}</span>
          <span @click=${this._toggleUnit} style="margin-left:8px;padding:2px 8px;font-size:11px;border-radius:10px;cursor:pointer;background:var(--secondary-background-color,#eee);color:var(--secondary-text-color);border:1px solid var(--divider-color,#ddd)">${"g"===this._unit?"→oz":"→g"}</span>
        </div>
        <div class="btn-group">
          <button class="btn btn-filled" @click=${this._addFood}>Add</button>
          <button class="btn btn-success" @click=${this._finishMeal}>Finish Meal</button>
          ${this._confirmReset?q`<button class="btn btn-danger" style="font-size:11px;padding:8px 12px" @click=${this._confirmResetAction}>Sure? (history kept)</button>`:q`<button class="btn btn-ghost" style="font-size:11px;padding:8px 12px" @click=${this._resetToday}>Clear Today</button>`}
        </div>
      </div>

      ${a?q`<div class="status-msg">${a}</div>`:""}

      ${n&&"Empty"!==n&&""!==n?q`
        <div class="section">
          <h3 class="section-title">Current Meal — ${Math.round(i)} kcal</h3>
          ${n.split(" | ").map(t=>q`<div class="log-item">${t}</div>`)}
        </div>
      `:""}

    `}_renderQuickAdd(t){const e=this._getState("text.thirdreality_smart_scale_meal_log"),i=this._getState("select.thirdreality_smart_scale_food_preset"),s=[],r=new Set;if(e&&"Empty"!==e)for(const i of e.split(" | ")){const e=i.match(/^(.+?)\s+\d+g=/);e&&t.includes(e[1])&&!r.has(e[1])&&(s.push(e[1]),r.add(e[1]))}i&&t.includes(i)&&!r.has(i)&&(s.push(i),r.add(i));const o=["Chicken Breast","Egg","Rice (cooked)","Banana","Apple","Salmon","Avocado","Oatmeal"];for(const e of o){if(s.length>=5)break;t.includes(e)&&!r.has(e)&&(s.push(e),r.add(e))}for(const e of t){if(s.length>=5)break;r.has(e)||(s.push(e),r.add(e))}return 0===s.length?"":q`
      <div style="display:flex;flex-wrap:wrap;gap:6px;margin-bottom:10px">
        ${s.slice(0,5).map(t=>q`
          <span @click=${()=>this._quickSelectFood(t)}
            style="padding:5px 12px;font-size:12px;border-radius:14px;cursor:pointer;
            background:${t===i?"var(--primary-color)":"var(--secondary-background-color,#f0f0f0)"};
            color:${t===i?"white":"var(--primary-text-color)"};
            border:1px solid ${t===i?"var(--primary-color)":"var(--divider-color,#ddd)"};
            transition:all 0.15s;user-select:none"
          >${t}</span>
        `)}
      </div>
    `}_quickSelectFood(t){this.hass.callService("select","select_option",{entity_id:"select.thirdreality_smart_scale_food_preset",option:t})}_renderTodayMeals(){const t=this._getState("text.thirdreality_smart_scale_calorie_history");if(!t)return"";const e=(new Date).toISOString().split("T")[0],i=this._parseHistory(t).find(t=>t.date===e);return i&&0!==i.meals.length?q`
      <div class="section">
        <h3 class="section-title">Today's Meals</h3>
        ${i.meals.map(t=>q`
          <div style="display:flex;align-items:center;padding:8px 0;border-bottom:1px solid var(--divider-color, #f0f0f0)">
            <span style="font-size:13px;font-weight:500;color:var(--primary-text-color);min-width:45px">${t.time}</span>
            <span style="flex:1"></span>
            <span style="font-size:13px;font-weight:600;color:var(--primary-color)">${t.cal} kcal</span>
          </div>
        `)}
      </div>
    `:""}_renderMiniHistory(t){const e=this._getState("text.thirdreality_smart_scale_calorie_history"),i=parseFloat(this._getState("number.thirdreality_smart_scale_today_calories"))||0,s=new Date,r=s.toISOString().split("T")[0],o={};if(e){const t=this._parseHistory(e);for(const e of t)o[e.date]=e.total}(i>0||o[r])&&(o[r]=Math.round(i)||o[r]||0);const a=[];for(let t=6;t>=0;t--){const e=new Date(s);e.setDate(e.getDate()-t);const i=e.toISOString().split("T")[0];a.push({date:i,total:o[i]||0})}return q`
      <div>
        <div class="mini-history-title">7-Day History</div>
        <div class="mini-history-chart">
          ${a.map(e=>{const i=e.total>0,s=i&&t>0?Math.min(Math.round(e.total/t*100),100):0,r=i?s>=100?"#f44336":s>=75?"#ff9800":"#4caf50":"var(--divider-color, #e0e0e0)",o=i?Math.max(.5*s,4):4;return q`
              <div class="mini-history-col">
                <span class="mini-history-label" style="font-weight:500;${i?"":"opacity:0.4"}">${i?e.total:"—"}</span>
                <div class="mini-history-bar-v" style="height:${o}px;background:${r}"></div>
                <span class="mini-history-label">${this._formatDateShort(e.date)}</span>
              </div>
            `})}
        </div>
      </div>
    `}_formatDateShort(t){try{const e=new Date;if(t===e.toISOString().split("T")[0])return"Tod";const i=new Date(e);if(i.setDate(i.getDate()-1),t===i.toISOString().split("T")[0])return"Yest";const s=new Date(t+"T00:00:00");return["Sun","Mon","Tue","Wed","Thu","Fri","Sat"][s.getDay()]}catch(e){return t.slice(-2)}}_getMotivation(t){const e=(new Date).getHours();return 0===t&&e<12?"🌅 Start your day — weigh your breakfast!":0===t?"📋 No meals tracked yet today":t<=25?"👍 Off to a good start":t<=50?"📊 On track — budget your next meal":t<=75?"⚡ More than halfway! Plan your dinner.":t<100?"⚠️ Almost at your limit — choose wisely":"✅ Daily target reached!"}_getStreak(){const t=this._getState("text.thirdreality_smart_scale_calorie_history");if(!t)return 0;const e=this._parseHistory(t),i=new Set(e.map(t=>t.date)),s=parseFloat(this._getState("number.thirdreality_smart_scale_today_calories"))||0,r=(new Date).toISOString().split("T")[0];s>0&&i.add(r);let o=0;const a=new Date;for(let t=0;t<30;t++){const t=a.toISOString().split("T")[0];if(!i.has(t))break;o++,a.setDate(a.getDate()-1)}return o}_getBestStreak(){const t=this._getState("text.thirdreality_smart_scale_calorie_history");if(!t)return 0;const e=this._parseHistory(t),i=new Set(e.map(t=>t.date));(parseFloat(this._getState("number.thirdreality_smart_scale_today_calories"))||0)>0&&i.add((new Date).toISOString().split("T")[0]);const s=[...i].sort();let r=0,o=0;for(let t=0;t<s.length;t++){if(0===t)o=1;else{const e=new Date(s[t-1]+"T00:00:00");o=1===(new Date(s[t]+"T00:00:00")-e)/864e5?o+1:1}o>r&&(r=o)}return r}_getWeekAvg(){const t=this._getState("text.thirdreality_smart_scale_calorie_history"),e=parseFloat(this._getState("number.thirdreality_smart_scale_today_calories"))||0,i=(new Date).toISOString().split("T")[0],s={};if(t){const e=this._parseHistory(t);for(const t of e)s[t.date]=t.total}e>0&&(s[i]=e);const r=new Date;let o=0,a=0;for(let t=0;t<7;t++){const e=new Date(r);e.setDate(e.getDate()-t);const i=e.toISOString().split("T")[0];s[i]&&s[i]>0&&(o+=s[i],a++)}return a>0?Math.round(o/a):0}_renderHistory(){const t=this._getState("text.thirdreality_smart_scale_calorie_history"),e=parseFloat(this._getState("number.thirdreality_smart_scale_daily_calorie_target"))||2e3;if(!t)return q`
        <div class="section">
          <div class="history-empty">
            <p style="font-size:32px;margin:0 0 12px">📊</p>
            <p>No calorie history yet.</p>
            <p style="font-size:12px">History is recorded when you finish a meal.</p>
          </div>
        </div>
      `;const i=this._parseHistory(t);return 0===i.length?q`
        <div class="section">
          <div class="history-empty">
            <p style="font-size:32px;margin:0 0 12px">📊</p>
            <p>No calorie history yet.</p>
            <p style="font-size:12px">History is recorded when you finish a meal.</p>
          </div>
        </div>
      `:q`
      <div class="section">
        <h3 class="section-title">Calorie History</h3>
        <p class="section-desc">Last ${i.length} day${i.length>1?"s":""} of tracked meals</p>
        ${i.map(t=>{const i=e>0?Math.min(Math.round(t.total/e*100),100):0,s=i>=100?"#f44336":i>=75?"#ff9800":"#4caf50";return q`
            <div class="history-day">
              <div class="history-day-header">
                <span class="history-date">${this._formatDate(t.date)}</span>
                <span class="history-total">${t.total} kcal</span>
              </div>
              <div class="history-bar">
                <div class="history-bar-fill" style="width:${i}%;background:${s}"></div>
              </div>
              ${t.meals.map(t=>q`
                <div class="history-meal">
                  <span class="history-meal-time">${t.time}</span>
                  <span class="history-meal-cal">${t.cal} kcal</span>
                </div>
              `)}
            </div>
          `})}
      </div>
    `}_parseHistory(t){if(!t)return[];const e=[];for(const i of t.split("|")){const t=i.split(":");if(t.length<2)continue;const s=t[0],r=parseInt(t[1])||0,o=t.slice(2).join(":"),a=[];if(o)for(const t of o.split(",")){const[e,i]=t.split("=");e&&i&&a.push({time:e,cal:parseInt(i)||0})}e.push({date:s,total:r,meals:a})}return e}_formatDate(t){try{const e=new Date;if(t===e.toISOString().split("T")[0])return"Today";const i=new Date(e);i.setDate(i.getDate()-1);if(t===i.toISOString().split("T")[0])return"Yesterday";const s=new Date(t+"T00:00:00");return`${["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"][s.getMonth()]} ${s.getDate()}`}catch(e){return t}}_renderRecipes(){return q`
      <div class="section">
        <h3 class="section-title">Add Recipe</h3>
        <p class="section-desc">Add a cocktail recipe. Format ingredients as: ingredient:weight,ingredient:weight</p>
        <input class="form-input" id="new-cocktail-name" placeholder="Cocktail name (e.g. Margarita)" style="margin-bottom:12px" />
        <input class="form-input" id="new-cocktail-ing" placeholder="Tequila:50,Triple Sec:30,Lime Juice:25" />
        <div class="btn-group">
          <button class="btn btn-filled" @click=${this._addCocktailItem}>Add Recipe</button>
        </div>
      </div>

      <div class="section">
        <h3 class="section-title">Remove Recipe</h3>
        <div class="form-row">
          <input class="form-input" id="remove-cocktail-name" placeholder="Cocktail name to remove" />
          <button class="btn btn-danger" @click=${this._removeCocktailItem}>Remove</button>
        </div>
      </div>
    `}_renderFoods(){return this._getState("sensor.thirdreality_smart_scale_weight"),q`
      <div class="section">
        <h3 class="section-title">Add Food</h3>
        <p class="section-desc">Add a food item to the calorie preset list.</p>
        <div style="display:flex;gap:8px">
          <input class="form-input" id="new-food-name" placeholder="Food name (e.g. Chicken Wings)" style="flex:2" />
          <input class="form-input" id="new-food-cal" type="number" placeholder="Cal/100g" style="flex:1" />
        </div>
        <div class="btn-group">
          <button class="btn btn-filled" @click=${this._addFoodItem}>Add Food</button>
        </div>
      </div>

      <div class="section">
        <h3 class="section-title">Remove Food</h3>
        <div class="form-row">
          <input class="form-input" id="remove-food-name" placeholder="Food name to remove" />
          <button class="btn btn-danger" @click=${this._removeFoodItem}>Remove</button>
        </div>
      </div>

    `}_getState(t){if(!this.hass?.states?.[t])return"";const e=this.hass.states[t].state;return"unknown"===e||"unavailable"===e?"":e}_getOptions(t){return this.hass?.states?.[t]?.attributes?.options||[]}_onCocktailSelect(t){this.hass.callService("select","select_option",{entity_id:"select.thirdreality_smart_scale_select_cocktail",option:t.target.value})}_onCustomRecipeChange(t){this.hass.callService("text","set_value",{entity_id:"text.thirdreality_smart_scale_custom_recipe",value:t.target.value})}_startCocktail(){this.hass.callService("button","press",{entity_id:"button.thirdreality_smart_scale_start_cocktail"})}_doneCocktail(){this.hass.callService("button","press",{entity_id:"button.thirdreality_smart_scale_done"})}_backToIdle(){this.hass.callService("select","select_option",{entity_id:"select.thirdreality_smart_scale_cocktail_step",option:"idle"})}_onFoodSearchInput(t){this._foodSearch=t.target.value}_filterFood(t){if(!this._foodSearch)return t;const e=this._foodSearch.toLowerCase();return t.filter(t=>t.toLowerCase().includes(e))}_selectFoodFromSearch(t){this._foodSearch=null,this.hass.callService("select","select_option",{entity_id:"select.thirdreality_smart_scale_food_preset",option:t})}_onFoodSelect(t){this.hass.callService("select","select_option",{entity_id:"select.thirdreality_smart_scale_food_preset",option:t.target.value})}_onCustomFoodNameChange(t){this.hass.callService("text","set_value",{entity_id:"text.thirdreality_smart_scale_custom_food_name",value:t.target.value})}_onCustomCalChange(t){this.hass.callService("number","set_value",{entity_id:"number.thirdreality_smart_scale_custom_cal_per_100g",value:parseFloat(t.target.value)||0})}_addFood(){this.hass.callService("button","press",{entity_id:"button.thirdreality_smart_scale_add_food"})}_finishMeal(){this.hass.callService("button","press",{entity_id:"button.thirdreality_smart_scale_finish_meal"})}_resetToday(){this._confirmReset=!0,setTimeout(()=>{this._confirmReset=!1},3e3)}_confirmResetAction(){this._confirmReset=!1,this.hass.callService("button","press",{entity_id:"button.thirdreality_smart_scale_reset_today"})}_onDailyTargetChange(t){this.hass.callService("number","set_value",{entity_id:"number.thirdreality_smart_scale_daily_calorie_target",value:parseFloat(t.target.value)||2e3})}_onMealWarningChange(t){this.hass.callService("number","set_value",{entity_id:"number.thirdreality_smart_scale_meal_calorie_warning",value:parseFloat(t.target.value)||800})}_addFoodItem(){const t=this.renderRoot.querySelector("#new-food-name")?.value?.trim(),e=parseFloat(this.renderRoot.querySelector("#new-food-cal")?.value)||0;!t||e<=0||(this.hass.callService("thirdreality_scale","add_food",{name:t,calories_per_100g:e}),this.renderRoot.querySelector("#new-food-name").value="",this.renderRoot.querySelector("#new-food-cal").value="")}_addCocktailItem(){const t=this.renderRoot.querySelector("#new-cocktail-name")?.value?.trim(),e=this.renderRoot.querySelector("#new-cocktail-ing")?.value?.trim();t&&e&&(this.hass.callService("thirdreality_scale","add_cocktail",{name:t,ingredients:e}),this.renderRoot.querySelector("#new-cocktail-name").value="",this.renderRoot.querySelector("#new-cocktail-ing").value="")}_removeFoodItem(){const t=this.renderRoot.querySelector("#remove-food-name")?.value?.trim();t&&(this.hass.callService("thirdreality_scale","remove_food",{name:t}),this.renderRoot.querySelector("#remove-food-name").value="")}_removeCocktailItem(){const t=this.renderRoot.querySelector("#remove-cocktail-name")?.value?.trim();t&&(this.hass.callService("thirdreality_scale","remove_cocktail",{name:t}),this.renderRoot.querySelector("#remove-cocktail-name").value="")}});
